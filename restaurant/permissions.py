from rest_framework import permissions


class RoleBasedPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.rol.id == 4:
            return True

        allowed_roles = {
            'IngredienteViewSet': [1, 2, 3],
            'CategoriaViewSet': [1, 2, 3],
            'PedidoViewSet': [1, 2, 3],
            'ProductoViewSet': [1, 2, 3],
        }

        return request.user.rol.id in allowed_roles.get(view.__class__.__name__, [])

    def has_object_permission(self, request, view, obj):
        if request.user.rol.id == 4:
            return True

        if view.__class__.__name__ == 'PedidosViewSet' and request.method in ['POST', 'PUT']:
            return request.user.rol.id in [1, 2, 3]

        return False
