from django.urls import path
from . import views

urlpatterns = [
    path('administrator/', views.dashboard, name='administrator'),
    path('inventory/', views.inventory, name='inventory'),
    path('report/', views.report, name='report'),
    path('income_expenses/', views.income_expenses, name='income_expenses'),
    path('stockHistory/', views.stockHistory, name='stockHistory'),
]