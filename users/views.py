from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request, 'users/login.html')
def signIn(request):
    return render(request, 'users/signIn.html')