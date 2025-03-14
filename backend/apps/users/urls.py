from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'profile', views.UserViewSet, basename='profile')


urlpatterns = [
    path('',include(router.urls)),
    path('telegram-auth/', views.TelegramAuthView.as_view(), name='telegram-auth'),
]