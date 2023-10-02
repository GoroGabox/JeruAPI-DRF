from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Ingrediente, Categoria, Producto, ProductoIngrediente, Pedido, PedidoProducto
from .serializers import IngredienteSerializer, CategoriaSerializer, ProductoSerializer, ProductoIngredienteSerializer, PedidoSerializer, PedidoProductoSerializer

# Create your views here.


class IngredienteViewSet(ModelViewSet):
    queryset = Ingrediente.objects.all()
    serializer_class = IngredienteSerializer


class CategoriaViewSet(ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class ProductoViewSet(ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer


class ProductoIngredienteViewSet(ModelViewSet):
    queryset = ProductoIngrediente.objects.all()
    serializer_class = ProductoIngredienteSerializer


class PedidoViewSet(ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer


class PedidoProductoViewSet(ModelViewSet):
    queryset = PedidoProducto.objects.all()
    serializer_class = PedidoProductoSerializer
