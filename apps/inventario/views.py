from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from .models import Producto, Categoria, Marca
from .serializers import ProductoSerializer, CategoriaSerializer, MarcaSerializer

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
    permission_classes = [IsAuthenticatedOrReadOnly]

class ResumenPorMarcaView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        resumen = Marca.objects.annotate(
            variedad_productos=Count('productos'),
            total_unidades=Sum('productos__stock_actual')
        ).values(
            'id',
            'nombre',
            'variedad_productos',
            'total_unidades'
        )

        return Response(resumen)

class RegistroUsuarioView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Debes enviar un "username" y un "password".'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Ese nombre de usuario ya esta registrado.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)
        return Response({
            'mensaje': f'Usuario {user.username} creado exitosamente.',
            'id': user.id,
            'username': user.username
        }, status=status.HTTP_201_CREATED)