from django.db.models.signals import pre_save, post_save, post_migrate
from django.dispatch import receiver
from django.dispatch import receiver
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django_apscheduler.models import DjangoJobExecution
from apscheduler.schedulers.background import BackgroundScheduler
from .models import PedidoProducto, ProductoIngrediente, Ingrediente, PedidoDiario


def reset_pedido_diario():
    PedidoDiario.objects.update(selected=False)
    print("Pedido diario reestablecido")


@receiver(post_migrate)
def start_scheduler(sender, **kwargs):
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(reset_pedido_diario, "cron", hour=16,
                      minute=0, id="reset_pedido_diario", replace_existing=True)
    register_events(scheduler)
    scheduler.start()


@receiver(pre_save, sender=PedidoProducto)
def set_precio_salida(sender, instance, **kwargs):
    instance.precio_salida = instance.producto.precio


@receiver(post_save, sender=PedidoProducto)
def update_stock(sender, instance, **kwargs):
    pedido_producto = instance
    producto = pedido_producto.producto
    cantidad_pedida = pedido_producto.cantidad

    for prod_ing in ProductoIngrediente.objects.filter(producto=producto):
        ing = prod_ing.ingrediente
        ing.cantidad_disponible -= prod_ing.cantidad * cantidad_pedida
        ing.save()
