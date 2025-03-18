from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeamViewSet, SubmissionViewSet

router = DefaultRouter()
router.register(r'teams', TeamViewSet)
router.register(r'submissions', SubmissionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]