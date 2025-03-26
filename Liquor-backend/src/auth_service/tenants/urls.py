from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TenantViewSet, BillingPlanViewSet, TenantBillingHistoryViewSet

router = DefaultRouter()
router.register(r'tenants', TenantViewSet)
router.register(r'billing/plans', BillingPlanViewSet)
router.register(r'billing/history', TenantBillingHistoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]