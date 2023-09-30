from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.views import UserModelViewSet, RolModelViewSet, MyTokenObtainPairView, UserRegisterView, LogOutAPIView

router = DefaultRouter()
router.register(r'users', UserModelViewSet, basename='users')
router.register(r'roles', RolModelViewSet, basename='roles')

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='login_view'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh_view'),
    path('logout/', LogOutAPIView.as_view(), name='logout_view'),
    path('register/', UserRegisterView.as_view(), name='register_view'),
] + router.urls