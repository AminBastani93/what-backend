from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Product
from .serializers import ProductSerializer, UserSerializer
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from .serializers import LoginRequestSerializer
from .serializers import CustomToken
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class AuthViewSet(viewsets.ViewSet):
    """
    ViewSet for handling authentication
    """
    permission_classes = []  # Allow unauthenticated access

    @swagger_auto_schema(
        request_body=LoginRequestSerializer,
        responses={200: UserSerializer,
                   400: "Invalid email format"}
    )
    @action(detail=False, methods=['post'])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            return Response(
                {"error": "Invalid email format"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create or get user using email as username
        username = email  # Generate username from email
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': username,
                'email': email
            }
        )
        if created:
            user.set_password(password)
            user.save()

        # Generate token
        refresh = CustomToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
        })

# Define the ProductViewSet to handle product-related actions
class ProductViewSet(ListModelMixin, GenericViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

# Define the product_list view to handle GET requests for all products
@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)