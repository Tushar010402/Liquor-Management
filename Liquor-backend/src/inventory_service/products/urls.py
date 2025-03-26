from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductCategoryViewSet, ProductTypeViewSet,
    ProductAttributeViewSet, ProductViewSet
)

router = DefaultRouter()
router.register(r'categories', ProductCategoryViewSet)
router.register(r'types', ProductTypeViewSet)
router.register(r'attributes', ProductAttributeViewSet)
router.register(r'', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
]