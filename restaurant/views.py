from django.shortcuts import render
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Ingrediente, Categoria, Producto, ProductoIngrediente, Pedido, PedidoProducto, EstadoPedido, PedidoDiario, AjusteStock
from .serializers import IngredienteSerializer, IngredienteSimpleSerializer, CategoriaSerializer, ProductoSerializer, ProductoIngredienteSerializer, ProductoSimpleSerializer, PedidoSerializer, PedidoProductoSerializer, EstadoPedidoSerializer, PedidoDiarioSerializer, AjusteStockSerializer
from rest_framework.permissions import IsAdminUser
from .permissions import RoleBasedPermission
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction


class EstadoPedidoViewSet(ModelViewSet):
    queryset = EstadoPedido.objects.all()
    serializer_class = EstadoPedidoSerializer


class IngredienteViewSet(ModelViewSet):
    queryset = Ingrediente.objects.all()
    serializer_class = IngredienteSerializer
    # permission_classes = [RoleBasedPermission]


class IngredienteSimpleViewSet(ModelViewSet):
    queryset = Ingrediente.objects.all()
    serializer_class = IngredienteSimpleSerializer


class IngredienteSimpleViewSet(ModelViewSet):
    queryset = Ingrediente.objects.all()
    serializer_class = IngredienteSimpleSerializer


class CategoriaViewSet(ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    # permission_classes = [RoleBasedPermission]


class ProductoViewSet(ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    # permission_classes = [RoleBasedPermission]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        if response.status_code == status.HTTP_201_CREATED:
            producto = response.data

        ingredientes = request.data.get('ingredientes', None)
        cantidades = request.data.get('cantidades', None)

        if ingredientes is not None and cantidades is not None:
            # valida que 'ingredientes' y 'cantidades' tengan la misma cantidad de elementos
            if len(ingredientes) != len(cantidades):
                return Response({'error': 'La cantidad de ingredientes y cantidades no coinciden'}, status=status.HTTP_400_BAD_REQUEST)

            # valida que los ingredientes existan
            for ingrediente in ingredientes:
                try:
                    Ingrediente.objects.get(pk=ingrediente)
                except Ingrediente.DoesNotExist:
                    return Response({'error': f'El ingrediente con id {ingrediente} no existe'}, status=status.HTTP_400_BAD_REQUEST)

            # valida que las cantidades son floats positivos
            for cantidad in cantidades:
                if not isinstance(cantidad, float) or cantidad < 0:
                    return Response({'error': 'Las cantidades deben ser numeros positivos'}, status=status.HTTP_400_BAD_REQUEST)

            # crea instancias de ProductoIngrediente con cantidades recibidas
            producto_obj = Producto.objects.get(pk=producto['id'])
            for ingrediente, cantidad in zip(ingredientes, cantidades):
                ingrediente = Ingrediente.objects.get(pk=ingrediente)
                ProductoIngrediente.objects.create(
                    ingrediente=ingrediente, producto=producto_obj, cantidad=cantidad)
        else:
            return Response({'error': "Se esperaban campos 'ingredientes' y 'cantidades'"}, status=status.HTTP_400_BAD_REQUEST)

        return response


class ProductoSimpleViewSet(ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSimpleSerializer


class ProductoIngredienteViewSet(ModelViewSet):
    queryset = ProductoIngrediente.objects.all()
    serializer_class = ProductoIngredienteSerializer
    # permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['producto', 'ingrediente']


class PedidoViewSet(ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    # permission_classes = [RoleBasedPermission]

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            pedido = self.get_object()
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "pedidos",
                {
                    "type": "send_pedido_update",
                    "action": "update",
                    "data": PedidoSerializer(pedido).data
                }
            )

        return response

    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            pedido = self.get_object()

            productos = request.data.get('productos', None)
            cantidades = request.data.get('cantidades', None)

            if productos is not None and cantidades is not None:
                # valida que 'productos' y 'cantidades' tengan la misma cantidad de elementos
                if len(productos) != len(cantidades):
                    return Response({'error': 'La cantidad de productos y cantidades no coinciden'}, status=status.HTTP_400_BAD_REQUEST)

                # valida que los productos existan
                for producto_id in productos:
                    try:
                        Producto.objects.get(pk=producto_id)
                    except Producto.DoesNotExist:
                        return Response({'error': f'El producto con id {producto_id} no existe'}, status=status.HTTP_400_BAD_REQUEST)

                # valida que las cantidades sean enteros positivos
                for cantidad in cantidades:
                    if not isinstance(cantidad, int) or cantidad < 0:
                        return Response({'error': 'Las cantidades deben ser enteros positivos'}, status=status.HTTP_400_BAD_REQUEST)

                # elimina todos los productos del pedido
                pedido.productos.clear()

                # crea instancias de PedidoProducto con cantidades recibidas
                for producto_id, cantidad in zip(productos, cantidades):
                    producto = Producto.objects.get(pk=producto_id)
                    PedidoProducto.objects.create(
                        producto=producto, pedido=pedido, cantidad=cantidad)

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "pedidos",
                {
                    "type": "send_pedido_update",
                    "action": "update",
                    "data": PedidoSerializer(pedido).data
                }
            )

        return response

    @transaction.atomic
    @action(detail=False, methods=['POST'])
    def create_pedido_with_productos(self, request):
        pedido_data = request.data

        # valida datos base de pedido
        serializer = self.get_serializer(data=pedido_data)
        if serializer.is_valid(raise_exception=True):
            pedido = serializer.save()

            # 'mesa' y 'nombre_cliente' son mutuamente excluyentes
            if 'mesa' in pedido_data and 'nombre_cliente' in pedido_data:
                Response({'error': 'Se esperaba solo uno de los campos "mesa" o "nombre_cliente"'},
                         status=status.HTTP_400_BAD_REQUEST)

            # 'productos' y 'cantidades' deben estar presentes
            if 'productos' not in pedido_data or 'cantidades' not in pedido_data:
                return Response({'error': "Se esperaban campos 'productos' y 'cantidades'"}, status=status.HTTP_400_BAD_REQUEST)
            # y por lo menos un par de 'productos' y 'cantidades'
            elif len(pedido_data['productos']) < 1:
                return Response({'error': "Se esperaba al menos un producto"}, status=status.HTTP_400_BAD_REQUEST)

            productos = pedido_data.pop('productos')
            cantidades = pedido_data.pop('cantidades')

            # 'productos' y 'cantidades' deben tener la misma cantidad de elementos
            if len(productos) != len(cantidades):
                return Response({'error': 'La cantidad de productos y cantidades no coinciden'}, status=status.HTTP_400_BAD_REQUEST)

            # crea instancias de PedidoProducto con cantidades recibidas
            for producto_id, cantidad in zip(productos, cantidades):
                producto = Producto.objects.get(pk=producto_id)
                PedidoProducto.objects.create(
                    producto=producto, pedido=pedido, cantidad=cantidad)

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "pedidos",
                {
                    "type": "send_pedido_update",
                    "action": "create",
                    "data": PedidoSerializer(pedido).data
                }
            )

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "pedido_updates",  # Group name
                {
                    "type": "send_pedido_action",
                    "action": "create",
                    "data": PedidoSerializer(pedido).data
                }
            )

            return Response(PedidoSerializer(pedido).data, status=status.HTTP_201_CREATED)


class PedidoProductoUpdateView(generics.UpdateAPIView):
    queryset = PedidoProducto.objects.all()
    serializer_class = PedidoProductoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['producto', 'pedido']


class PedidoProductoDeleteView(generics.DestroyAPIView):
    queryset = PedidoProducto.objects.all()
    serializer_class = PedidoProductoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['producto', 'pedido']


class PedidoProductoViewSet(ModelViewSet):
    queryset = PedidoProducto.objects.all()
    serializer_class = PedidoProductoSerializer
    # permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['producto', 'pedido']


class PedidoDiarioViewSet(ModelViewSet):
    queryset = PedidoDiario.objects.all()
    serializer_class = PedidoDiarioSerializer


class AjusteStockViewSet(ModelViewSet):
    queryset = AjusteStock.objects.all()
    serializer_class = AjusteStockSerializer
    # permission_classes = [IsAdminUser]
