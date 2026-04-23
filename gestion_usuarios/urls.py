# gestion_usuarios/urls.py
from django.urls import path
from .views import listar_usuarios, crear_usuario, eliminar_usuario

urlpatterns = [
    path('usuarios/', listar_usuarios, name='usuarios-list'),
    path('usuarios/crear/', crear_usuario, name='usuarios-create'),
    path('usuarios/eliminar/<str:username>/', eliminar_usuario, name='usuarios-delete'),
]