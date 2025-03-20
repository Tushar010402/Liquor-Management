from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountTypeViewSet, AccountViewSet, FiscalYearViewSet, AccountingPeriodViewSet, BankAccountViewSet

router = DefaultRouter()
router.register(r'types', AccountTypeViewSet)
router.register(r'chart', AccountViewSet)
router.register(r'fiscal-years', FiscalYearViewSet)
router.register(r'periods', AccountingPeriodViewSet)
router.register(r'bank-accounts', BankAccountViewSet)

urlpatterns = [
    path('', include(router.urls)),
]