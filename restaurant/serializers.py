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
    precio = serializers.ReadOnlyField(source='producto.precio')
    id = serializers.IntegerField(write_only=True)

    class Meta:
        model = PedidoProducto
        fields = ['id', 'producto', 'nombre', 'cantidad', 'precio']


class PedidoSerializer(serializers.ModelSerializer):
    productos = serializers.SerializerMethodField()
    productos_post = PedidoProductoDetalleSerializer(
        many=True, write_only=True)

    class Meta:
        model = Pedido
        fields = '__all__'

    def get_productos(self, obj):
        queryset = PedidoProducto.objects.filter(pedido=obj)
        serializer = PedidoProductoDetalleSerializer(queryset, many=True)
        return serializer.data

    def create(self, validated_data):
        productos_data = validated_data.pop('productos_post')
        if not productos_data:
            raise serializers.ValidationError(
                "Un pedido debe tener al menos un producto")
        pedido = Pedido.objects.create(**validated_data)

        for producto_data in productos_data:
            producto = Producto.objects.get(id=producto_data['id'])
            PedidoProducto.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=producto_data['cantidad'],
                precio_salida=producto.precio),
        return pedido

    def update(self, pedido, validated_data):
        # Crea instancia de Pedido
        pedido.estado = validated_data.get('estado', pedido.estado)
        pedido.mesa = validated_data.get('mesa', pedido.mesa)
        pedido.usuario = validated_data.get('usuario', pedido.usuario)
        pedido.save()

        # Revisa si hay productos en el pedido
        productos_data = validated_data.pop('productos_post', [])
        productos_existentes = PedidoProducto.objects.filter(
            pedido=pedido).count()
        if not productos_data and productos_existentes == 0:
            raise serializers.ValidationError(
                "Un pedido debe tener al menos un producto")

        # Actualiza los productos del pedido
        for producto_data in productos_data:
            producto_id = producto_data.get('id')
            cantidad = producto_data.get('cantidad')
            try:
                producto = Producto.objects.get(id=producto_id)
            except Producto.DoesNotExist:
                raise serializers.ValidationError(
                    f"No existe un Producto con ID {producto_id}.")

            pedido_producto, created = PedidoProducto.objects.get_or_create(
                pedido=pedido,
                producto=producto,
                defaults={'cantidad': cantidad,
                          'precio_salida': producto.precio}
            )

            if not created:
                pedido_producto.cantidad = cantidad
                pedido_producto.precio_salida = producto.precio
                pedido_producto.save()

        return pedido
