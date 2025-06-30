from django.urls import path
from . import views

urlpatterns = [
    path('accountant/', views.dashboard, name='accountant'),
    path('income/add/', views.income, name='income'),
    path('expense/add/', views.expenses, name='expenses'),
    path('income/report/', views.income_report, name='income_report'),
    path('expense/report/', views.expense_report, name='expense_report'),
    path('my_records/', views.my_records, name='my_records'),
    path('summary/', views.reports, name='reports'),
]