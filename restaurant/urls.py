from rest_framework.routers import DefaultRouter
from restaurant.views import IngredienteViewSet, CategoriaViewSet, ProductoViewSet, ProductoIngredienteViewSet, PedidoViewSet, PedidoProductoViewSet

router = DefaultRouter()
router.register(r'ingredientes', IngredienteViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'productos-ingredientes', ProductoIngredienteViewSet)
router.register(r'pedidos', PedidoViewSet)
router.register(r'pedidos-productos', PedidoProductoViewSet)

urlpatterns = router.urls
