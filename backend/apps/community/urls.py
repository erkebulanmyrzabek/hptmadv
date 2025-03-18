from django.urls import path
from . import views

router = routers.DefaultRouter()
router.register(r'teams', views.TeamViewSet)

urlpatterns = [
    path('', include(router.urls)),
]