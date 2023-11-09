from django.shortcuts import render
from django.db import transaction
from rest_framework.viewsets import ModelViewSet
from .models import Ingrediente, Categoria, Producto, ProductoIngrediente, Pedido, PedidoProducto, EstadoPedido
from .serializers import IngredienteSerializer, IngredienteSimpleSerializer, CategoriaSerializer, ProductoSerializer, ProductoIngredienteSerializer, ProductoSimpleSerializer, PedidoSerializer, PedidoProductoSerializer, EstadoPedidoSerializer
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

class PedidoProductoViewSet(ModelViewSet):
    queryset = PedidoProducto.objects.all()
    serializer_class = PedidoProductoSerializer
    # permission_classes = [IsAdminUser]
