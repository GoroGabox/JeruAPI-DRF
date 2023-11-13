from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


class EstadoPedido(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


class Ingrediente(models.Model):
    nombre = models.CharField(max_length=255)
    cantidad_disponible = models.PositiveIntegerField()
    cantidad_critica = models.PositiveIntegerField()
    unidad = models.CharField(max_length=16)

    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    abreviacion = models.CharField(max_length=10)
    precio = models.PositiveIntegerField()
    ingredientes = models.ManyToManyField(
        Ingrediente, through='ProductoIngrediente')

    def __str__(self):
        return self.nombre


class ProductoIngrediente(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()


class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=255)
    nombre_cliente = models.CharField(max_length=255, null=True)
    mesa = models.PositiveIntegerField(null=True)
    productos = models.ManyToManyField(Producto, through='PedidoProducto')

    def __str__(self):
        return f'{self.usuario} #{self.id}'


class PedidoProducto(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_salida = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False)


class PedidoDiario(models.Model):
    nombre = models.CharField(max_length=255)
    selected = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre, self.selected


class AjusteStock(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    tipo_ajuste = models.CharField(max_length=255)
    cantidad = models.PositiveIntegerField()
    motivo = models.CharField(max_length=255)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.producto} {self.tipo_ajuste} {self.cantidad}'
