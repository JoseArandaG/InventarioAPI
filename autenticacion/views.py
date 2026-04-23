from django.shortcuts import render

# Create your views here.
from django.db import connection
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
@permission_classes([AllowAny])
def login_api_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM public.login_usuario(%s, %s)", [username, password])
            row = cursor.fetchone()
            if row and row[0] == "Login exitoso":
                token = RefreshToken()
                token['username'] = row[2]
                token['rol'] = row[4]
                return Response({
                    "mensaje": row[0],
                    "token": {"access": str(token.access_token), "refresh": str(token)},
                    "user": {"id": row[1], "nombre": row[3], "rol": row[4]}
                }, status=status.HTTP_200_OK)
            return Response({"error": row[0] if row else "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({"error_tecnico": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)