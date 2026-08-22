from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from apps.inventario.registro import RegistroUsuarioView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/inventario/', include('apps.inventario.urls')),
    path('api/register/', RegistroUsuarioView.as_view(), name='api_register'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),       
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
