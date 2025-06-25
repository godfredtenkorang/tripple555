from django.urls import path
from . import views

urlpatterns = [
    path('accountant/', views.dashboard, name='accountant')
]