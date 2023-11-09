from rest_framework import serializers
from restaurant.models import Ingrediente, Categoria, Producto, Pedido, PedidoProducto, EstadoPedido, ProductoIngrediente


class EstadoPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoPedido
        fields = '__all__'


class IngredienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingrediente
        fields = '__all__'

class IngredienteSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingrediente
        fields = ['nombre']


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProductoIngredienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoIngrediente
        fields = ['nombre', 'cantidad']

class ProductoSerializer(serializers.ModelSerializer):
    ingredientes = ProductoIngredienteSerializer(many=True)

    class Meta:
        model = Producto
        fields = '__all__'

class ProductoSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Producto
        exclude = ['ingredientes']

class PedidoProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoProducto
        fields = '__all__'

class PedidoProductoDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoProducto
        fields = '__all__'


class PedidoSerializer(serializers.ModelSerializer):
    productos = ProductoSerializer(many=True)

    class Meta:
        model = Pedido
        fields = '__all__'