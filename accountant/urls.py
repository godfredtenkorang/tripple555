from django.urls import path
from . import views

urlpatterns = [
    path('accountant/', views.dashboard, name='accountant'),
    path('income/', views.income, name='income'),
    path('expenses/', views.expenses, name='expenses'),
    path('reports/', views.reports, name='reports'),
]