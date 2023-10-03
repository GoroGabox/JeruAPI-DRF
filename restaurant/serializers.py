from rest_framework import serializers
from restaurant.models import Ingrediente, Categoria, Producto, ProductoIngrediente, Pedido, PedidoProducto, EstadoPedido

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
    ingredientes = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = '__all__'

    def get_ingredientes(self, obj):
        queryset = obj.ingredientes.all()
        serializer = IngredienteSimpleSerializer(queryset, many=True)
        return serializer.data
    
class ProductoSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Producto
        exclude = ['ingredientes']


class ProductoIngredienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoIngrediente
        fields = '__all__'


class PedidoSerializer(serializers.ModelSerializer):
    productos = serializers.SerializerMethodField()

    class Meta:
        model = Pedido
        fields = '__all__'
    
    def get_productos(self, obj):
        queryset = obj.productos.all()
        serializer = ProductoSimpleSerializer(queryset, many=True)
        return serializer.data


class PedidoProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoProducto
        fields = '__all__'
