from django.shortcuts import render

# Create your views here.
from django.db import connection
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
@permission_classes([AllowAny]) # Permitir que cualquiera intente loguearse
def login_api_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM public.login_usuario(%s, %s)", [username, password])
            row = cursor.fetchone()

            if row:
                mensaje = row[0]
                
                if mensaje == "Login exitoso":
                    # Extraemos datos
                    user_id = row[1]
                    user_name = row[2]
                    rol = row[4]

                    # GENERACIÓN DEL TOKEN MANUAL
                    # Usamos el ID de tu tabla de Supabase como 'user_id' en el token
                    token = RefreshToken()
                    # Podemos meter datos extra (payload) en el token
                    token['username'] = user_name
                    token['rol'] = rol
                    token['user_id'] = user_id

                    return Response({
                        "mensaje": mensaje,
                        "token": {
                            "refresh": str(token),
                            "access": str(token.access_token),
                        },
                        "user": {
                            "id": user_id,
                            "nombre": row[3],
                            "rol": rol
                        }
                    }, status=status.HTTP_200_OK)
                
                else:
                    return Response({"error": mensaje}, status=status.HTTP_401_UNAUTHORIZED)
            
            return Response({"error": "No se recibió respuesta del servidor"}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({"error_tecnico": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)