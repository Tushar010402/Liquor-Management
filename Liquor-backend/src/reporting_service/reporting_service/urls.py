from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Reporting Service API",
        default_version='v1',
        description="API documentation for the Reporting Service",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # Add other URL patterns here
    # path('api/sales-reports/', include('reporting_service.sales_reports.urls')),
    # path('api/inventory-reports/', include('reporting_service.inventory_reports.urls')),
    # path('api/financial-reports/', include('reporting_service.financial_reports.urls')),
    # path('api/tax-reports/', include('reporting_service.tax_reports.urls')),
    # path('api/performance-reports/', include('reporting_service.performance_reports.urls')),
    # path('api/dashboards/', include('reporting_service.dashboards.urls')),
    # path('api/analytics/', include('reporting_service.analytics.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 