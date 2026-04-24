"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.urls import path
from django.shortcuts import render

# Funciones simples para renderizar tus archivos
def login_view(request):
    return render(request, 'login.html')

def admin_view(request):
    return render(request, 'admin_dashboard.html')

def operator_view(request):
    return render(request, 'operador_dashboard.html')

urlpatterns = [
    path('api/auth/', include('autenticacion.urls')),      # login/
    path('api/gestion/', include('gestion_usuarios.urls')), # usuarios/, eliminar/, etc.
    path('login/', login_view, name='login'),
    path('admin-dashboard/', admin_view, name='admin_dashboard'),
    path('operator-dashboard/', operator_view, name='operator_dashboard'),
]