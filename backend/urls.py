from django.urls import path, include
from rest_framework.routers import DefaultRouter
from products.views import AuthViewSet, ProductViewSet
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="What Products API",
        default_version='v1',
        description="API for getting products and authentication",
        terms_of_service="#",
        contact=openapi.Contact(email="aminbastani@outlook.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]