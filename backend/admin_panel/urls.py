from django.urls import path
from .views import admin_login, admin_dashboard, manage_hackathons, manage_users, analytics, admin_logout

urlpatterns = [
    path('', admin_login, name='admin_login'),
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('manage-hackathons/', manage_hackathons, name='manage_hackathons'),
    path('manage-users/', manage_users, name='manage_users'),
    path('analytics/', analytics, name='analytics'),
    path('logout/', admin_logout, name='admin_logout'),
]