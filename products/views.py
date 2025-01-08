from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product
from .serializers import ProductSerializer, UserSerializer
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import api_view

class AuthViewSet(viewsets.ViewSet):
    """
    ViewSet for handling authentication
    """
    permission_classes = []  # Allow unauthenticated access

    @action(detail=False, methods=['post'])
    def login(self, request):
        """
        Login endpoint that accepts any credentials
        """
        username = request.data.get('username')
        password = request.data.get('password')

        # Create or get user (for task purposes)
        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': f'{username}@example.com'}
        )
        if created:
            user.set_password(password)
            user.save()

        login(request, user)
        return Response(UserSerializer(user).data)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        """
        Logout endpoint
        """
        logout(request)
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def current_user(self, request):
        """
        Get current user information
        """
        if request.user.is_authenticated:
            return Response(UserSerializer(request.user).data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class ProductViewSet(ListModelMixin, GenericViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)