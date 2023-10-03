from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Ingrediente, Categoria, Producto, ProductoIngrediente, Pedido, PedidoProducto, EstadoPedido
from .serializers import IngredienteSerializer, IngredienteSimpleSerializer, CategoriaSerializer, ProductoSerializer, ProductoIngredienteSerializer, ProductoSimpleSerializer, PedidoSerializer, PedidoProductoSerializer, EstadoPedidoSerializer

# Create your views here.

class EstadoPedidoViewSet(ModelViewSet):
    queryset = EstadoPedido.objects.all()
    serializer_class = EstadoPedidoSerializer


class IngredienteViewSet(ModelViewSet):
    queryset = Ingrediente.objects.all()
    serializer_class = IngredienteSerializer

class IngredienteSimpleViewSet(ModelViewSet):
    queryset = Ingrediente.objects.all()
    serializer_class = IngredienteSimpleSerializer


class CategoriaViewSet(ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class ProductoViewSet(ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class ProductoSimpleViewSet(ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSimpleSerializer


class ProductoIngredienteViewSet(ModelViewSet):
    queryset = ProductoIngrediente.objects.all()
    serializer_class = ProductoIngredienteSerializer


class PedidoViewSet(ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer


class PedidoProductoViewSet(ModelViewSet):
    queryset = PedidoProducto.objects.all()
    serializer_class = PedidoProductoSerializer
