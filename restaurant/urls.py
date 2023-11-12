from django.urls import path
from rest_framework.routers import DefaultRouter
from restaurant.views import IngredienteViewSet, IngredienteSimpleViewSet, CategoriaViewSet, ProductoViewSet, ProductoIngredienteViewSet, PedidoViewSet, PedidoProductoViewSet, EstadoPedidoViewSet, ProductoSimpleViewSet, PedidoProductoUpdateView, PedidoProductoDeleteView, PedidoDiarioViewSet

router = DefaultRouter()
router.register(r'ingredientes', IngredienteViewSet)
router.register(r'ingredientes-simple', IngredienteSimpleViewSet,
                basename='Ingredientes-simple')
router.register(r'categorias', CategoriaViewSet)
router.register(r'productos', ProductoViewSet, basename='productos')
router.register(r'productos-simple', ProductoSimpleViewSet,
                basename='productos-simple')
router.register(r'productos-ingredientes', ProductoIngredienteViewSet)
router.register(r'pedidos', PedidoViewSet)
router.register(r'pedidos-productos', PedidoProductoViewSet)
router.register(r'estado-pedido', EstadoPedidoViewSet)
router.register(r'pedido-diario', PedidoDiarioViewSet)

generics_urls = [
    path('pedidos/<int:pedido_id>/productos/<int:producto_id>/',
         PedidoProductoUpdateView.as_view(), name='pedido-producto-update'),
    path('pedidos/<int:pedido_id>/productos/<int:producto_id>/',
         PedidoProductoDeleteView.as_view(), name='pedido-producto-delete'),
]

urlpatterns = generics_urls + router.urls
