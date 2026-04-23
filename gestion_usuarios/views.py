from django.shortcuts import render

# Create your views here.
from django.db import connection
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


# Usuarios
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
            # Al ser una función que devuelve TEXT, usamos SELECT
            cursor.execute("SELECT public.sp_usuario_eliminar(%s)", [username])
            
            # fetchone() trae la fila, [0] trae el contenido del texto devuelto
            resultado = cursor.fetchone()
            
        return Response({
            "mensaje": resultado[0]
        }, status=status.HTTP_200_OK)

    except Exception as e:
        # Capturamos el error personalizado del RAISE EXCEPTION
        # Limpiamos el mensaje para mostrar solo la primera línea del error de Postgres
        error_completo = str(e)
        error_limpio = error_completo.split('\n')[0]
        
        return Response({
            "error": error_limpio
        }, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def actualizar_usuario(request):
    d = request.data
    params = [d.get('username'), d.get('nombre'), d.get('apellido'), d.get('direccion'), d.get('correo'), d.get('telefono')]
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT public.sp_usuario_actualizar(%s,%s,%s,%s,%s,%s)", params)
        return Response({"mensaje": "Usuario actualizado correctamente"})
    except Exception as e:
        return Response({"error": str(e)}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def gestionar_bloqueo(request):
    username = request.data.get('username')
    bloquear = request.data.get('bloquear') # Enviar true o false
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT public.sp_usuario_gestionar_bloqueo(%s, %s)", [username, bloquear])
            res = cursor.fetchone()
        return Response({"resultado": res[0]})
    except Exception as e:
        return Response({"error": str(e)}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cambiar_password(request):
    d = request.data
    params = [d.get('username'), d.get('password_actual'), d.get('nueva_password')]
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM public.sp_usuario_cambiar_password(%s, %s, %s)", params)
            row = cursor.fetchone()
        return Response({"resultado": row[0], "mensaje": row[1]})
    except Exception as e:
        return Response({"error": str(e)}, status=400)



#Roles
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_roles(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM public.sp_rol_listar()")
            columns = [col[0] for col in cursor.description]
            resultados = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return Response(resultados, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_rol(request):
    nombre = request.data.get('nombre_rol')
    descripcion = request.data.get('descripcion_rol')
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM public.sp_rol_crear(%s, %s)", [nombre, descripcion])
            row = cursor.fetchone()
        return Response({"id_rol": row[0], "mensaje": row[1]}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def actualizar_rol(request):
    id_rol = request.data.get('id_rol')
    nombre = request.data.get('nombre_rol')
    descripcion = request.data.get('descripcion_rol')
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT public.sp_rol_actualizar(%s, %s, %s)", [id_rol, nombre, descripcion])
            mensaje = cursor.fetchone()
        return Response({"mensaje": mensaje[0]})
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminar_rol(request, id_rol):
    try:
        with connection.cursor() as cursor:
            # Llamamos a la función
            cursor.execute("SELECT public.sp_rol_eliminar(%s)", [id_rol])
            mensaje = cursor.fetchone()
            
        return Response({"mensaje": mensaje[0]}, status=status.HTTP_200_OK)
        
    except Exception as e:
        # Aquí capturamos el mensaje de 'RAISE EXCEPTION' de la base de datos
        # Limpiamos el error para no enviar todo el log técnico
        error_msg = str(e).split('\n')[0] 
        return Response({"error": error_msg}, status=status.HTTP_400_BAD_REQUEST)