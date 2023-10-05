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


class ProductoIngredienteSerializer(serializers.ModelSerializer):
    nombre = serializers.ReadOnlyField(source='ingrediente.nombre')

    class Meta:
        model = ProductoIngrediente
        fields = ['nombre', 'cantidad']


class ProductoSerializer(serializers.ModelSerializer):
    ingredientes = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = '__all__'

    def get_ingredientes(self, obj):
        queryset = ProductoIngrediente.objects.filter(producto=obj)
        serializer = ProductoIngredienteSerializer(queryset, many=True)
        return serializer.data


class ProductoSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Producto
        exclude = ['ingredientes']


class PedidoProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoProducto
        fields = '__all__'


class PedidoProductoDetalleSerializer(serializers.ModelSerializer):
    producto = serializers.ReadOnlyField(source='producto.id')
    nombre = serializers.ReadOnlyField(source='producto.nombre')

    class Meta:
        model = PedidoProducto
        fields = ['producto', 'nombre', 'cantidad']


class PedidoSerializer(serializers.ModelSerializer):
    productos = PedidoProductoDetalleSerializer(many=True)

    class Meta:
        model = Pedido
        fields = '__all__'

    def create(self, validated_data):
        productos_data = validated_data.pop('productos')
        pedido = Pedido.objects.create(**validated_data)
        for producto_data in productos_data:
            producto_id = producto_data.get('id')
            producto = Producto.objects.get(id=producto_id)
            PedidoProducto.objects.create(
                pedido=pedido, producto=producto, cantidad=producto_data.get('cantidad'))
        return pedido

    def get_productos(self, obj):
        queryset = PedidoProducto.objects.filter(pedido=obj)
        serializer = PedidoProductoDetalleSerializer(queryset, many=True)
        return serializer.data
