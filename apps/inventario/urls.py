from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AsistenteIAView, CategoriaViewSet, MarcaViewSet, ProductoViewSet, ResumenPorMarcaView, RealizarCompraView

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'marcas', MarcaViewSet)
router.register(r'productos', ProductoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('resumen-marcas/', ResumenPorMarcaView.as_view(), name='resumen-marcas'),
    path('asistente-ia/', AsistenteIAView.as_view(), name='asistente-ia'),
    path('comprar-producto/', RealizarCompraView.as_view(), name='comprar-producto'),
]