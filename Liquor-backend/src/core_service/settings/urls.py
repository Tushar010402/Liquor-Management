from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SystemSettingViewSet, TenantSettingViewSet,
    EmailTemplateViewSet, NotificationTemplateViewSet
)

router = DefaultRouter()
router.register(r'system', SystemSettingViewSet)
router.register(r'tenant', TenantSettingViewSet)
router.register(r'email-templates', EmailTemplateViewSet)
router.register(r'notification-templates', NotificationTemplateViewSet)

urlpatterns = [
    path('', include(router.urls)),
]