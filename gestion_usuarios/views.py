from django.shortcuts import render

# Create your views here.
from django.db import connection
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_usuarios(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM public.sp_usuario_listar()")
            columns = [col[0] for col in cursor.description]
            resultados = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return Response(resultados)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_usuario(request):
    d = request.data
    params = [d.get('nombre'), d.get('apellido'), d.get('password'), d.get('direccion'), d.get('correo'), d.get('telefono')]
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM public.sp_usuario_crear(%s,%s,%s,%s,%s,%s)", params)
            row = cursor.fetchone()
        return Response({"mensaje": "Creado", "username": row[0]}, status=201)
    except Exception as e:
        return Response({"error": str(e)}, status=400)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminar_usuario(request, username):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT public.sp_usuario_eliminar(%s)", [username])
        return Response({"mensaje": f"Usuario {username} eliminado"})
    except Exception as e:
        return Response({"error": str(e)}, status=400)