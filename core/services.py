import datetime
from datetime import date
from typing import Optional, Tuple
from django.utils import timezone
from .models import Espaco, Usuario, Remanejamento, ReservaPontual, ReservaFixa


class ValidadorReservaService:

    @classmethod
    def validar_direito_retirada(
        cls,
        espaco: Espaco,
        usuario: Usuario,
        dt_referencia: date = None,
        hr_referencia: datetime.time = None,
    ) -> Tuple[bool, str]:
        agora = timezone.localtime()
        dt_referencia = dt_referencia or agora.date()
        hr_referencia = hr_referencia or agora.time().replace(microsecond=0)

        titular, origem = cls._quem_ganha_a_chave(espaco, dt_referencia, hr_referencia)

        if titular is None:
            return True, "Retirada autorizada: espaço livre no período."

        if titular.pk == usuario.pk:
            return True, f"Retirada autorizada: direito do usuário por {origem}."

        return False, (
            f"Retirada negada: o espaço está alocado a outro usuário "
            f"({titular}) por {origem}."
        )

    @classmethod
    def _quem_ganha_a_chave(
        cls, espaco: Espaco, dt: date, hr: datetime.time
    ) -> Tuple[Optional[Usuario], Optional[str]]:
        rem = (
            Remanejamento.objects.filter(
                espaco=espaco,
                dt_remanejamento=dt,
                hr_inicio__lte=hr,
                hr_fim__gt=hr,
            )
            .select_related("usuario_substituto")
            .first()
        )
        if rem:
            return rem.usuario_substituto, "REMANEJAMENTO"

        pontual = (
            ReservaPontual.objects.filter(
                espaco=espaco,
                dt_reserva=dt,
                st_aprovado=True,
                hr_inicio__lte=hr,
                hr_fim__gt=hr,
            )
            .select_related("usuario")
            .first()
        )
        if pontual:
            return pontual.usuario, pontual.tp_reserva

        fixa = (
            ReservaFixa.objects.filter(
                espaco=espaco,
                nr_dia_semana=dt.weekday(),
                hr_inicio__lte=hr,
                hr_fim__gt=hr,
            )
            .select_related("usuario")
            .first()
        )
        if fixa:
            return fixa.usuario, "FIXA"

        return None, None