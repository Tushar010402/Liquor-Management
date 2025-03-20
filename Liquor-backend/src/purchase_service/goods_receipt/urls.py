from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GoodsReceiptViewSet, QualityCheckViewSet

router = DefaultRouter()
router.register(r'receipts', GoodsReceiptViewSet)
router.register(r'quality-checks', QualityCheckViewSet)

urlpatterns = [
    path('', include(router.urls)),
]