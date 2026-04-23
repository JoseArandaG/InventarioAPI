# autenticacion/authentication.py
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User

class SupabaseJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        # Extraemos el ID de Supabase del token
        user_id = validated_token.get("sub")
        
        # Creamos un objeto de usuario "al aire" (sin guardarlo en DB)
        # Esto engaña a Django para que crea que hay alguien logueado
        user = User(username=user_id)
        user.is_active = True
        return user