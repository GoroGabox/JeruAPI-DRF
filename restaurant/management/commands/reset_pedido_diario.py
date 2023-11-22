from django.core.management.base import BaseCommand
from restaurant.models import PedidoDiario


class Command(BaseCommand):
    help = 'Reestablece el pedido diario'

    def handle(self, *args, **options):
        PedidoDiario.objects.update(selected=False)
        self.stdout.write(self.style.SUCCESS('Pedido diario reestablecido'))
