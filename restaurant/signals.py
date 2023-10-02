from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import PedidoProducto, ProductoIngrediente, Ingrediente


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
