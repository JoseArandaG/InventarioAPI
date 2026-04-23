# gestion_usuarios/urls.py
from django.urls import path
from .views import (
    listar_usuarios, 
    crear_usuario, 
    actualizar_usuario, 
    eliminar_usuario, 
    gestionar_bloqueo,
    cambiar_password,
    # Endpoints de Roles
    listar_roles, 
    crear_rol, 
    actualizar_rol, 
    eliminar_rol,
    #Endpoints de Permisos
    listar_permisos,
    crear_permiso,
    actualizar_permiso,
    eliminar_permiso
)

urlpatterns = [
    # Gestión de Usuarios
    path('usuarios/', listar_usuarios, name='usuarios-list'),
    path('usuarios/crear/', crear_usuario, name='usuarios-create'),
    path('usuarios/actualizar/', actualizar_usuario, name='usuarios-update'),
    path('usuarios/eliminar/<str:username>/', eliminar_usuario, name='usuarios-delete'),
    path('usuarios/bloqueo/', gestionar_bloqueo, name='usuarios-bloqueo'),
    path('usuarios/password/', cambiar_password, name='usuarios-password'),

    # Gestión de Roles
    path('roles/', listar_roles, name='roles-list'),
    path('roles/crear/', crear_rol, name='roles-create'),
    path('roles/actualizar/', actualizar_rol, name='roles-update'),
    path('roles/eliminar/<int:id_rol>/', eliminar_rol, name='roles-delete'),
    
    #Gestión de Permisos
    path('permisos/', listar_permisos, name='permisos-list'),
    path('permisos/crear/', crear_permiso, name='permisos-create'),
    path('permisos/actualizar/', actualizar_permiso, name='permisos-update'), # <--- Añade esta
    path('permisos/eliminar/<int:id_permiso>/', eliminar_permiso, name='permisos-delete'),
]