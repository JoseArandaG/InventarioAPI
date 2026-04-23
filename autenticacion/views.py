from django.shortcuts import render

# Create your views here.
from django.db import connection
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def login_api_view(request):
    """
    Recibe username y password, llama al SP en Supabase y retorna el resultado.
    """
    username = request.data.get('username')
    password = request.data.get('password')

    # Validación básica de entrada
    if not username or not password:
        return Response(
            {"mensaje_salida": "Debe proporcionar usuario y contraseña."}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        with connection.cursor() as cursor:
            # Ejecutamos tu función de Supabase
            cursor.execute("SELECT * FROM login_usuario(%s, %s)", [username, password])
            
            # Recuperamos la fila (RETURNS TABLE)
            row = cursor.fetchone()

            if row:
                # El orden depende de los campos de tu RETURNS TABLE en SQL
                data = {
                    "mensaje": row[0],
                    "id_usuario": row[1],
                    "username": row[2],
                    "nombre_completo": row[3],
                    "rol": row[4],
                    "fecha_acceso": row[5]
                }

                # Si el SP dice que el login es exitoso
                if row[0] == "Login exitoso":
                    return Response(data, status=status.HTTP_200_OK)
                else:
                    # Mensajes de: "Contraseña incorrecta", "Usuario bloqueado", etc.
                    return Response(data, status=status.HTTP_401_UNAUTHORIZED)
            
            return Response({"mensaje": "Error en la consulta"}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)