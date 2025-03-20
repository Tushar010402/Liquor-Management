from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# API documentation schema
schema_view = get_schema_view(
    openapi.Info(
        title="Liquor Shop Management - Inventory Service API",
        default_version='v1',
        description="API documentation for the Inventory Service of Liquor Shop Management System",
        terms_of_service="https://www.liquorshop.com/terms/",
        contact=openapi.Contact(email="contact@liquorshop.com"),
        license=openapi.License(name="Proprietary License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # Health check
    path('', include('common.urls')),
    
    # API endpoints
    path('api/inventory/brands/', include('brands.urls')),
    path('api/inventory/products/', include('products.urls')),
    path('api/inventory/suppliers/', include('suppliers.urls')),
    path('api/inventory/stock/', include('stock.urls')),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)