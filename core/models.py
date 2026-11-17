from django.db import models


class DiaSemana(models.IntegerChoices):
    SEGUNDA = 0, "Segunda-feira"
    TERCA = 1, "Terça-feira"
    QUARTA = 2, "Quarta-feira"
    QUINTA = 3, "Quinta-feira"
    SEXTA = 4, "Sexta-feira"
    SABADO = 5, "Sábado"


class ReservaFixa(models.Model):
    nr_dia_semana = models.IntegerField(choices=DiaSemana.choices)
    hr_inicio = models.TimeField()
    hr_fim = models.TimeField()
    ds_turma = models.CharField()



class Unidade(models.Model):
    """Representa cada escola do SENAI."""

    id_unidade = models.AutoField(primary_key=True)
    cd_unidade = models.CharField(
        max_length=20, unique=True)  # ex: 'SENAI-APAR'
    # ex: 'SENAI Aparecida de Goiânia'
    nm_unidade = models.CharField(max_length=150)
    cidade = models.CharField(max_length=100, default="Aparecida de Goiânia")

    class Meta:
        db_table = "unidade"
        verbose_name = "Unidade"
        verbose_name_plural = "Unidades"

    def __str__(self):
        return f"{self.cd_unidade} - {self.nm_unidade}"


class Usuario(models.Model):
    """Docentes, coordenadores e administradores."""

    class Perfil(models.TextChoices):
        MASTER_GERAL = "MASTER_GERAL", "Master Geral"
        MASTER_UNIDADE = "MASTER_UNIDADE", "Master da Unidade"
        COORDENADOR = "COORDENADOR", "Coordenador"
        DOCENTE = "DOCENTE", "Docente"
        PORTARIA = "PORTARIA", "Portaria"

    id_usuario = models.AutoField(primary_key=True)
    nm_usuario = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    uuid_cracha = models.CharField(
        max_length=50, unique=True, null=True, blank=True)
    perfil = models.CharField(max_length=20, choices=Perfil.choices)
    unidades = models.ManyToManyField(Unidade, related_name="usuarios")  # N:N
    st_ativo = models.BooleanField(default=True)

    class Meta:
        db_table = "usuario"
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return f"{self.nm_usuario} ({self.perfil})"


class Espaco(models.Model):
    """Laboratórios e salas de aula pertencentes a uma unidade."""

    id_espaco = models.AutoField(primary_key=True)
    unidade = models.ForeignKey(
        Unidade,
        on_delete=models.PROTECT,  # impede excluir unidade que tenha espaços
        related_name="espacos",
    )
    # ex: 'Lab. 03 de Informática'
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
    espaco = models.OneToOneField(
        Espaco,
        on_delete=models.PROTECT,  # impede excluir espaço que tenha chave
        related_name="chave",
    )
    cd_chave = models.CharField(
        max_length=30, unique=True)       # ex: 'CH-LAB03'
    uuid_tag_chave = models.CharField(
        max_length=50, unique=True)  # leitor RFID
    st_disponivel = models.BooleanField(default=True)

    class Meta:
        db_table = "chave"
        verbose_name = "Chave"
        verbose_name_plural = "Chaves"

    def __str__(self):
        return f"{self.cd_chave} -> {self.espaco.ds_espaco}"
