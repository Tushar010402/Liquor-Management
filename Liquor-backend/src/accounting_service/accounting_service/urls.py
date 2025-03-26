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
        title="Liquor Shop Management - Accounting Service API",
        default_version='v1',
        description="API documentation for the Accounting Service of Liquor Shop Management System",
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
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # Health check
    path('', include('common.urls')),
    
    # API endpoints
    path('api/accounts/', include('accounts.urls')),
    path('api/journals/', include('journals.urls')),
    path('api/ledger/', include('ledger.urls')),
    path('api/reports/', include('reports.urls')),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)