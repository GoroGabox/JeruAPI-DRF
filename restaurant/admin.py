from django.contrib import admin
from .models import PedidoProducto, Ingrediente, Categoria, Producto, ProductoIngrediente, Pedido


class PedidoProductoAdmin(admin.ModelAdmin):
    readonly_fields = ('precio_salida',)


admin.site.register(Ingrediente)
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(ProductoIngrediente)
admin.site.register(Pedido)
admin.site.register(PedidoProducto, PedidoProductoAdmin)
