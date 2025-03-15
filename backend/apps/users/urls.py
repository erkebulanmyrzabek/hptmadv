from django.urls import path, include
from .views import TelegramAuthView, UserViewSet, UserUpdateView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'profile', UserViewSet, basename='user')

urlpatterns = [
    path('telegram-auth/', TelegramAuthView.as_view(), name='telegram-auth'),
    path('profile/update/', UserUpdateView.as_view(), name='user-update'),
    path('', include(router.urls)),
]