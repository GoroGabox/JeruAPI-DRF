from rest_framework import serializers
from restaurant.models import Ingrediente, Categoria, Producto, Pedido, PedidoProducto, EstadoPedido, ProductoIngrediente, PedidoDiario


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


class ProductoSerializer(serializers.ModelSerializer):
    ingredientes = IngredienteSerializer(many=True)

    class Meta:
        model = Producto
        fields = '__all__'


class PedidoSerializer(serializers.ModelSerializer):
    productos = ProductoSerializer(many=True)

    class Meta:
        model = Pedido
        fields = '__all__'


class ProductoSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['nombre']


class ProductoIngredienteSerializer(serializers.ModelSerializer):
    producto = ProductoSimpleSerializer()
    ingrediente = IngredienteSimpleSerializer()

    class Meta:
        model = ProductoIngrediente
        fields = '__all__'


class PedidoProductoSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer()
    pedido = PedidoSerializer()

    class Meta:
        model = PedidoProducto
        fields = '__all__'


class PedidoDiarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoDiario
        fields = '__all__'
