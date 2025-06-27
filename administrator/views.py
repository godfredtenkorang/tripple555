from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, 'administrator/dashboard.html')

def inventory(request):
    return render(request, 'administrator/inventory.html')

def report(request):
    return render(request, 'administrator/report.html')

def income_expenses(request):
    return render(request, 'administrator/income_expenses.html')

def stockHistory(request):
    return render(request, 'administrator/stockHistory.html')