
from django.urls import path
from .views import TelegramLoginView

urlpatterns = [
    path('api/login/telegram/', TelegramLoginView.as_view(), name='telegram-login'),
]