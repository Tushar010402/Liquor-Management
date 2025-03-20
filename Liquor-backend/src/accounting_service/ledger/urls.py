from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GeneralLedgerViewSet, AccountBalanceViewSet, TrialBalanceViewSet

router = DefaultRouter()
router.register(r'general', GeneralLedgerViewSet)
router.register(r'balances', AccountBalanceViewSet)
router.register(r'trial-balance', TrialBalanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]