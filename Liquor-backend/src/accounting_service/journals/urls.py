from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JournalViewSet, RecurringJournalViewSet

router = DefaultRouter()
router.register(r'', JournalViewSet)
router.register(r'recurring', RecurringJournalViewSet)

urlpatterns = [
    path('', include(router.urls)),
]