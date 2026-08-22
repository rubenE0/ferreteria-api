from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User

class RegistroUsuarioView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({'error': 'Usuario y contraseña requeridos.'}, status=status.HTTP_400_BAD_REQUEST)
            
        if User.objects.filter(username=username).exists():
            return Response({'error': 'El usuario ya existe.'}, status=status.HTTP_400_BAD_REQUEST)
            
        User.objects.create_user(username=username, password=password)
        return Response({
            'mensaje': 'Usuario registrado exitosamente.',
            'nombre_usuario': username,
            'contraseña': password,

        }, status=status.HTTP_201_CREATED)