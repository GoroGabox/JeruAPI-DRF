from django.shortcuts import render
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from .models import Ingrediente, Categoria, Producto, ProductoIngrediente, Pedido, PedidoProducto, EstadoPedido
from .serializers import IngredienteSerializer, IngredienteSimpleSerializer, CategoriaSerializer, ProductoSerializer, ProductoIngredienteSerializer, ProductoSimpleSerializer, PedidoSerializer, PedidoProductoSerializer, EstadoPedidoSerializer, PedidoSimpleSerializer
from rest_framework.permissions import IsAdminUser
from .permissions import RoleBasedPermission

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


class ProductoSimpleViewSet(ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSimpleSerializer


class ProductoSimpleViewSet(ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSimpleSerializer


class ProductoIngredienteViewSet(ModelViewSet):
    queryset = ProductoIngrediente.objects.all()
    serializer_class = ProductoIngredienteSerializer
    # permission_classes = [IsAdminUser]


class PedidoViewSet(ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    # permission_classes = [RoleBasedPermission]

    @action(detail=False, methods=['post'])
    def create_pedido_with_productos(self, request):
        pedido_data = request.data
        productos_ids = pedido_data.pop('productos', [])
        serializer = self.get_serializer(data=pedido_data)

        if serializer.is_valid(raise_exception=True):
            pedido = serializer.save()

            productos = Producto.objects.filter(id__in=productos_ids)
            pedido.productos.set(productos)

            return Response(PedidoSerializer(pedido).data, status=status.HTTP_201_CREATED)
        
    #Espera recibir los productos como una lista de IDs    
    # {
    #     ...
    #     "nombre_cliente": "Nombre del Cliente",
    #     "mesa": 5,
    #     "productos": [1, 2, 3]  // Lista de IDs de productos
    # }

class PedidoProductoUpdateView(generics.UpdateAPIView):
    queryset = PedidoProducto.objects.all()
    serializer_class = PedidoProductoSerializer

class PedidoProductoDeleteView(generics.DestroyAPIView):
    queryset = PedidoProducto.objects.all()
    serializer_class = PedidoProductoSerializer


class PedidoProductoViewSet(ModelViewSet):
    queryset = PedidoProducto.objects.all()
    serializer_class = PedidoProductoSerializer
    # permission_classes = [IsAdminUser]
