from django.utils import timezone
from .models import ReservaFixa, ReservaPontual, Remanejamento


def quem_ganha_a_chave(espaco, momento=None):
    """Retorna (usuario, origem) ou (None, None) se o espaço estiver livre."""
    momento = timezone.localtime(momento or timezone.now())
    hoje, agora = momento.date(), momento.time()


    rem = Remanejamento.objects.filter(
        espaco=espaco, dt_remanejamento=hoje,
        hr_inicio__lte=agora, hr_fim__gt=agora,
    ).select_related("usuario_substituto").first()
    if rem:
        return rem.usuario_substituto, "REMANEJAMENTO"

    pontual = ReservaPontual.objects.filter(
        espaco=espaco, dt_reserva=hoje, st_aprovado=True,
        hr_inicio__lte=agora, hr_fim__gt=agora,
    ).select_related("usuario").first()
    if pontual:
        return pontual.usuario, pontual.tp_reserva

    
    fixa = ReservaFixa.objects.filter(
        espaco=espaco, nr_dia_semana=hoje.weekday(),
        hr_inicio__lte=agora, hr_fim__gt=agora,
    ).select_related("usuario").first()
    if fixa:
        return fixa.usuario, "FIXA"

    
    return None, None

    class validadorRersevaService:
        @classmethod 
        def validar_direito_retirada(
            cls,
            espacp: Espaco,
            usuario: Usuario,
            dt_referencia: date = Nome,
            hr_referencia: datetime.time = NotImplemented
        )