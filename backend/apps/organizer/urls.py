from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrganizerHackathonViewSet

router = DefaultRouter()
router.register(r'hackathons', OrganizerHackathonViewSet, basename='organizer-hackathons')

urlpatterns = [
    path('', include(router.urls)),
]