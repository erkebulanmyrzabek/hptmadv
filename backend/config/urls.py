from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.events.views import HackathonViewSet
from django.contrib import admin

urlpatterns = [
    path('', include('apps.users.urls')),
    path('', include('apps.events.urls')),
    path('admin/', admin.site.urls),
]