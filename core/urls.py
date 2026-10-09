from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('programs/', views.programs_view, name='programs'),
    path('team/', views.team_view, name='team'),
    path('apply/', views.volunteer_view, name='volunteer'),
]