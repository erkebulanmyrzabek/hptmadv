from django.urls import path
from . import views

urlpatterns = [
    path('', views.TeamListView.as_view(), name='team-list'),
    path('<int:pk>/', views.TeamDetailView.as_view(), name='team-detail'),
    path('create/', views.TeamCreateView.as_view(), name='team-create'),
    path('<int:pk>/join/', views.TeamJoinView.as_view(), name='team-join'),
    path('<int:pk>/leave/', views.TeamLeaveView.as_view(), name='team-leave'),
]