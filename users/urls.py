from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('signIn', views.signIn, name='signIn')
]