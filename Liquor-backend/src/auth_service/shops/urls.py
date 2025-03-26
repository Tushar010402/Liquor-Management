from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShopViewSet, ShopSettingsViewSet

router = DefaultRouter()
router.register(r'shops', ShopViewSet)
router.register(r'shop-settings', ShopSettingsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]