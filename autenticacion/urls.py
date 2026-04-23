from django.urls import path
from .views import login_api_view

urlpatterns = [
    path('login/', login_api_view, name='api-login'),
]