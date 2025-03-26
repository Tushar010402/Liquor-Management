from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FinancialReportViewSet, ReportScheduleViewSet, ReportTemplateViewSet

router = DefaultRouter()
router.register(r'', FinancialReportViewSet)
router.register(r'schedules', ReportScheduleViewSet)
router.register(r'templates', ReportTemplateViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('profit-loss/', FinancialReportViewSet.as_view({'get': 'profit_loss'}), name='profit-loss-report'),
    path('balance-sheet/', FinancialReportViewSet.as_view({'get': 'balance_sheet'}), name='balance-sheet-report'),
    path('cash-flow/', FinancialReportViewSet.as_view({'get': 'cash_flow'}), name='cash-flow-report'),
]