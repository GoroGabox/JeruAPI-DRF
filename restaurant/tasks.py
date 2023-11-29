from .models import PedidoDiario
from celery import shared_task


@shared_task
def reset_pedido_diario():
    PedidoDiario.objects.update(selected=False)
    print('Pedido diario fue reseteado')
