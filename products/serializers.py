from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product
from drf_yasg import openapi
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class LoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(
        help_text="User's email address"
    )
    password = serializers.CharField(
        write_only=True,
        help_text="User's password",
        style={'input_type': 'password'}
    )

    class Meta:
        swagger_schema_fields = {
            "type": openapi.TYPE_OBJECT,
            "title": "Login Request",
            "properties": {
                "email": {
                    "type": "string",
                    "format": "email"
                },
                "password": {
                    "type": "string",
                    "format": "password"
                }
            },
            "required": ["email", "password"]
        }

class CustomToken(RefreshToken):
    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)        
        token['email'] = user.email        
        return token
    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'stock')

