from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import auth
from .models import User
# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            
            if user.role == "ADMIN":
                return redirect("administrator")
            elif user.role == "ACCOUNTANT":
                return redirect("accountant")

            
        else:
            messages.error(request, 'Invalid password.')
            return redirect('login')
        
    context = {
      
        'title': 'Login'
    }
    return render(request, 'users/login.html', context)

def signIn(request):
    return render(request, 'users/signIn.html')


def logout(request):
    
    auth.logout(request)
    return redirect('login')