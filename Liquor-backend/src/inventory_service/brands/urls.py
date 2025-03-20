from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BrandCategoryViewSet, BrandViewSet

router = DefaultRouter()
router.register(r'categories', BrandCategoryViewSet)
router.register(r'', BrandViewSet)

urlpatterns = [
    path('', include(router.urls)),
]