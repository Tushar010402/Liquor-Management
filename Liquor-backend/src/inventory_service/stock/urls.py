from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StockLevelViewSet, StockTransactionViewSet,
    StockTransferViewSet, StockAdjustmentViewSet
)

router = DefaultRouter()
router.register(r'levels', StockLevelViewSet)
router.register(r'transactions', StockTransactionViewSet)
router.register(r'transfers', StockTransferViewSet)
router.register(r'adjustments', StockAdjustmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]