from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SupplierViewSet, SupplierProductViewSet, SupplierPaymentViewSet, SupplierInvoiceViewSet

router = DefaultRouter()
router.register(r'', SupplierViewSet)
router.register(r'products', SupplierProductViewSet)
router.register(r'payments', SupplierPaymentViewSet)
router.register(r'invoices', SupplierInvoiceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]