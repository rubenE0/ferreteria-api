from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count
from .models import Producto, Categoria, Marca
from .serializers import ProductoSerializer, CategoriaSerializer, MarcaSerializer
from .services_ia import consultar_asistente_inventario

# Create your views here.
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]

class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    permission_classes = [IsAuthenticated]

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]

class ResumenPorMarcaView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        resumen = list(Marca.objects.annotate(
            variedad_productos=Count('productos'),
            total_unidades=Sum('productos__stock_actual')
        ).values(
            'id',
            'nombre',
            'variedad_productos',
            'total_unidades'
        ))

        for n in resumen:
            if n['total_unidades'] is None:
                n['total_unidades'] = 0

        return Response(resumen)

class RealizarCompraView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        producto_id = request.data.get('producto_id')
        cantidad = int(request.data.get('cantidad', 1))

        if not producto_id or not cantidad:
            return Response({'error': 'Producto y cantidad requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            producto = Producto.objects.get(id=producto_id)
        except Producto.DoesNotExist:
            return Response({'error': 'Producto no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        if producto.stock_actual < cantidad:
            return Response({f"error: Stock insuficiente. Disponible: {producto.stock_actual}"}, status=status.HTTP_400_BAD_REQUEST)

        producto.stock_actual -= cantidad
        producto.save()

        return Response({'mensaje': 'Compra realizada exitosamente.',
                         'producto': producto.nombre,
                         'cantidad': cantidad,
                         'stock_restante': producto.stock_actual
                         }, status=status.HTTP_200_OK)

class AsistenteIAView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        pregunta = request.data.get('pregunta', '')

        if not pregunta:
            return Response({'error': 'Debes enviar una "pregunta".'}, status=status.HTTP_400_BAD_REQUEST)

        resultado = consultar_asistente_inventario(pregunta)
        return Response({
            'Pregunta': pregunta,
            'Respuesta': resultado}, status=status.HTTP_200_OK)