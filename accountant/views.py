from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, 'accountant/dashboard.html')

def income(request):
    return render(request, 'accountant/income.html')

def expenses(request):
    return render(request, 'accountant/expenses.html')