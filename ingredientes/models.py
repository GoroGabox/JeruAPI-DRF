from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Ingrediente(models.Model):
    nombre = models.CharField(max_length=255)
    cantidad_disponible = models.PositiveIntegerField()
    cantidad_critica = models.PositiveIntegerField()

class Categoria(models.Model):
    nombre = models.CharField(max_length=255)

class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

class ProductoIngrediente(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)

class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=255)
    nombre_cliente = models.CharField(max_length=255)

class PedidoProducto(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_salida = models.DecimalField(max_digits=10, decimal_places=2)