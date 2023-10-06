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
        print(f"validated_data: {validated_data}")
        productos_data = validated_data.pop('productos_post')
        print(f"productos_data: {productos_data}")
        pedido = Pedido.objects.create(**validated_data)

        for producto_data in productos_data:
            producto = Producto.objects.get(id=producto_data['id'])
            PedidoProducto.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=producto_data['cantidad'],
                precio_salida=producto.precio),
        return pedido

    def update(self, instance, validated_data):
        instance.estado = validated_data.get('estado', instance.estado)
        instance.mesa = validated_data.get('mesa', instance.mesa)
        instance.usuario = validated_data.get('usuario', instance.usuario)
        instance.save()

        productos_data = validated_data.pop('productos_post', [])
        for producto_data in productos_data:
            producto_id = producto_data.get('id')
            cantidad = producto_data.get('cantidad')
            try:
                producto = Producto.objects.get(id=producto_id)
            except Producto.DoesNotExist:
                raise serializers.ValidationError(
                    f"Producto with ID {producto_id} does not exist.")

            pedido_producto, created = PedidoProducto.objects.get_or_create(
                pedido=instance,
                producto=producto,
                defaults={'cantidad': cantidad,
                          'precio_salida': producto.precio}
            )

            if not created:
                pedido_producto.cantidad = cantidad
                pedido_producto.precio_salida = producto.precio
                pedido_producto.save()

        return instance
