from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class PerfilAcesso(models.TextChoices):
    MASTER_GERAL = 'MASTER_GERAL', 'Master Geral (Global)'
    MASTER_UNIDADE = 'MASTER_UNIDADE', 'Master da Unidade'
    COORDENADOR = 'COORDENADOR', 'Coordenador de Área'
    DOCENTE = 'DOCENTE', 'Docente'
    PORTARIA = 'PORTARIA', 'Operador de Portaria'


class DiaSemana(models.IntegerChoices):
    SEGUNDA = 0, "Segunda-feira"
    TERCA = 1, "Terça-feira"
    QUARTA = 2, "Quarta-feira"
    QUINTA = 3, "Quinta-feira"
    SEXTA = 4, "Sexta-feira"
    SABADO = 5, "Sábado"


class TipoReservaPontual(models.TextChoices):
    DOCENTE_PONTUAL = "DOCENTE_PONTUAL", "Reserva Esporádica de Docente"
    EVENTO_EXTERNO = "EVENTO_EXTERNO", "Evento Institucional / Externo"
    MANUTENCAO = "MANUTENCAO", "Manutenção / Bloqueio Técnico"


class Unidade(models.Model):
    """Representa cada escola do SENAI."""

    id_unidade = models.AutoField(primary_key=True)
    cd_unidade = models.CharField(max_length=20, unique=True)  # ex: 'SENAI-APAR'
    nm_unidade = models.CharField(max_length=150)
    cidade = models.CharField(max_length=100, default="Aparecida de Goiânia")

    class Meta:
        db_table = "unidade"
        verbose_name = "Unidade"
        verbose_name_plural = "Unidades"

    def __str__(self):
        return f"{self.cd_unidade} - {self.nm_unidade}"


class Usuario(AbstractUser):
    """Docentes, coordenadores e administradores."""

    perfil = models.CharField(
        max_length=20,
        choices=PerfilAcesso.choices,
        default=PerfilAcesso.DOCENTE,
    )
    uuid_cracha = models.CharField(max_length=50, unique=True, null=True, blank=True)
    unidades = models.ManyToManyField(Unidade, related_name="usuarios", blank=True)

    class Meta:
        db_table = "usuario"
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.perfil})"


class Espaco(models.Model):
    """Laboratórios e salas de aula pertencentes a uma unidade."""

    id_espaco = models.AutoField(primary_key=True)
    unidade = models.ForeignKey(Unidade, on_delete=models.PROTECT, related_name="espacos")
    ds_espaco = models.CharField(max_length=150)
    st_disponivel = models.BooleanField(default=True)

    class Meta:
        db_table = "espaco"
        verbose_name = "Espaço"
        verbose_name_plural = "Espaços"

    def __str__(self):
        return f"{self.ds_espaco} [{self.unidade.cd_unidade}]"


class Chave(models.Model):
    """Tag RFID e código da chave associada a um espaço."""

    id_chave = models.AutoField(primary_key=True)
    espaco = models.OneToOneField(Espaco, on_delete=models.PROTECT, related_name="chave")
    cd_chave = models.CharField(max_length=30, unique=True)
    uuid_tag_chave = models.CharField(max_length=50, unique=True)
    st_disponivel = models.BooleanField(default=True)

    class Meta:
        db_table = "chave"
        verbose_name = "Chave"
        verbose_name_plural = "Chaves"

    def __str__(self):
        return f"{self.cd_chave} -> {self.espaco.ds_espaco}"


class ReservaFixa(models.Model):
    """Grade semanal oficial (recorrente)."""

    id_reserva_fixa = models.AutoField(primary_key=True)
    espaco = models.ForeignKey(Espaco, on_delete=models.CASCADE, related_name="reservas_fixas")
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name="reservas_fixas")
    nr_dia_semana = models.IntegerField(choices=DiaSemana.choices)
    hr_inicio = models.TimeField()
    hr_fim = models.TimeField()
    ds_turma = models.CharField(max_length=100)

    class Meta:
        db_table = "reserva_fixa"
        verbose_name = "Reserva Fixa"
        verbose_name_plural = "Reservas Fixas"
        unique_together = ("espaco", "nr_dia_semana", "hr_inicio")
        ordering = ["nr_dia_semana", "hr_inicio"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(hr_fim__gt=models.F("hr_inicio")),
                name="ck_reserva_fixa_fim_apos_inicio",
            )
        ]

    def clean(self):
        if self.hr_inicio and self.hr_fim and self.hr_fim <= self.hr_inicio:
            raise ValidationError("A hora de fim deve ser posterior à hora de início.")

    def __str__(self):
        return f"{self.ds_turma} | {self.get_nr_dia_semana_display()} {self.hr_inicio:%H:%M}"


class ReservaPontual(models.Model):
    id_reserva_pontual = models.AutoField(primary_key=True)
    espaco = models.ForeignKey(
        Espaco, on_delete=models.CASCADE,
        related_name="reservas_pontuais", verbose_name="Espaço",
    )
    usuario = models.ForeignKey(
        Usuario, on_delete=models.PROTECT,
        related_name="reservas_pontuais", verbose_name="Usuário",
    )
    dt_reserva = models.DateField(verbose_name="Data da Reserva")
    hr_inicio = models.TimeField(verbose_name="Hora de Início")
    hr_fim = models.TimeField(verbose_name="Hora de Fim")
    tp_reserva = models.CharField(
        max_length=20, choices=TipoReservaPontual.choices, verbose_name="Tipo de Reserva",
    )
    ds_motivo = models.TextField(verbose_name="Motivo / Justificativa")
    st_aprovado = models.BooleanField(default=False, verbose_name="Aprovado")

    class Meta:
        db_table = "tb_reserva_pontual"
        verbose_name = "Reserva Pontual"
        verbose_name_plural = "Reservas Pontuais"
        ordering = ["dt_reserva", "hr_inicio"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(hr_fim__gt=models.F("hr_inicio")),
                name="ck_reserva_pontual_fim_apos_inicio",
            )
        ]

    def clean(self):
        if self.hr_inicio and self.hr_fim and self.hr_fim <= self.hr_inicio:
            raise ValidationError("A hora de fim deve ser posterior à hora de início.")

    def __str__(self):
        return f"{self.get_tp_reserva_display()} | {self.espaco.ds_espaco} | {self.dt_reserva} {self.hr_inicio:%H:%M}"


class Remanejamento(models.Model):
    id_remanejamento = models.AutoField(primary_key=True)
    espaco = models.ForeignKey(
        Espaco, on_delete=models.CASCADE,
        related_name="remanejamentos", verbose_name="Espaço",
    )
    usuario_substituto = models.ForeignKey(
        Usuario, on_delete=models.PROTECT,
        related_name="remanejamentos_recebidos", verbose_name="Usuário Substituto",
    )
    dt_remanejamento = models.DateField(verbose_name="Data Específica da Alteração")
    hr_inicio = models.TimeField(verbose_name="Hora de Início")
    hr_fim = models.TimeField(verbose_name="Hora de Fim")
    tp_reserva = models.CharField(
        max_length=20, choices=TipoReservaPontual.choices,
        default=TipoReservaPontual.DOCENTE_PONTUAL, verbose_name="Tipo de Reserva",
    )
    ds_motivo = models.TextField(verbose_name="Motivo do Remanejamento")
    dh_registro = models.DateTimeField(auto_now_add=True, verbose_name="Data/Hora do Registro")

    class Meta:
        db_table = "tb_remanejamento"
        verbose_name = "Remanejamento"
        verbose_name_plural = "Remanejamentos"
        ordering = ["-dt_remanejamento", "hr_inicio"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(hr_fim__gt=models.F("hr_inicio")),
                name="ck_remanejamento_fim_apos_inicio",
            )
        ]

    def clean(self):
        if self.hr_inicio and self.hr_fim and self.hr_fim <= self.hr_inicio:
            raise ValidationError("A hora de fim deve ser posterior à hora de início.")

    def __str__(self):
        nome = self.usuario_substituto.get_full_name() or self.usuario_substituto.username
        return f"Remanejamento {self.dt_remanejamento} | {self.espaco.ds_espaco} -> {nome}"