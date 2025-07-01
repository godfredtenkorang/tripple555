import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from administrator.models import Battery
from .models import Income, Expense
from .forms import IncomeForm, ExpenseForm
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib import messages
from django.db.models import Sum, Count

# Create your views here.
def dashboard(request):
    today = timezone.now().date()
    start_of_month  = today.replace(day=1)
    
    batteries = Battery.objects.all()
    low_stock_battery = [b for b in batteries if b.is_low_stock]
    
    # Income/Expense calculations
    
    
    return render(request, 'accountant/dashboard.html')

# @login_required
def income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.created_by = request.user
            
        # If it's a battery sale, update stock
        if income.income_type == 'battery_sale' and income.battery:
            battery = income.battery
            if battery.quantity > 0:
                battery.quantity -= 1
                battery.save()
            else:
                messages.error(request, 'Selected battery is out of stock!')
                return redirect('income')
            
        income.save()
        messages.success(request, 'Income record added successfully!')
        return redirect('accountant')
    
    else:
        form = IncomeForm
    
    return render(request, 'accountant/income.html', {'form': form})

# @login_required
def expenses(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.created_by = request.user
            expense.save()
            messages.success(request, 'Expense record added successfully!')
            return redirect('accountant')
        
    else:
        form = ExpenseForm()
    return render(request, 'accountant/expenses.html', {'form': form})

# @login_required
def income_report(request):
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    incomes = Income.objects.all()
    
    incomes = incomes.filter(created_by=request.user)
    
    if date_from:
        incomes = incomes.filter(created_at__date__gte=date_from)
    if date_to:
        incomes = incomes.filter(created_at__date__lte=date_to)
        
    total = incomes.aggregate(total=Sum('amount'))['total'] or 0
    
    context = {
        'incomes': incomes,
        'total': total,
        'date_from': date_from,
        'date_to': date_to
    }
    
    return render(request, 'accountant/income_report.html', context)

# @login_required
def expense_report(request):
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    expenses = Expense.objects.all()
    
    expenses = expenses.filter(created_by=request.user)
    
    if date_from:
        expenses = expenses.filter(created_at__date__gte=date_from)
    if date_to:
        expenses = expenses.filter(created_at__date__lte=date_to)
        
    total = expenses.aggregate(total=Sum('amount'))['total'] or 0
    
    context = {
        'expenses': expenses,
        'total': total,
        'date_from': date_from,
        'date_to': date_to
    }
    
    return render(request, 'accountant/expense_report.html', context)

def my_records(request):
    
    return render(request, 'accountant/my_records.html')

# @login_required
def reports(request):
    # Get time period from request (day, month, year)
    period = request.GET.get('period', 'month')
    now = timezone.now()
    
    if period == 'day':
        date_from = now.date()
        date_to = now.date()
        period_name = "Today"
    elif period == 'month':
        date_from = now.replace(day=1).date()
        date_to = now.date()
        period_name = "This Month"
    elif period == 'year':
        date_from = now.replace(month=1, day=1).date()
        date_to = now.date()
        period_name = "This Year"
    else:
        # Custom date range
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        if date_from and date_to:
            date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
            date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
            period_name = f"{date_from.strftime('%b %d, %Y')} to {date_to.strftime('%b %d, %Y')}"
        else:
            date_from = None
            date_to = None
            period_name = "All Time"
        
    incomes = Income.objects.all()
    expenses = Expense.objects.all()
    
    # Apply date filters if specified
    if date_from and date_to:
        incomes = incomes.filter(created_at__date__range=[date_from, date_to])
        expenses = expenses.filter(created_at__date__range=[date_from, date_to])
        
    # Calculate totals
    income_total = incomes.aggregate(total=Sum('amount'))['total'] or 0
    expense_total = expenses.aggregate(total=Sum('amount'))['total'] or 0
    
    profit = income_total - expense_total
    
    # Get income by type
    income_by_type = incomes.values('income_type').annotate(
        total=Sum('amount'),
        count=Count('id')
    ).order_by('-total')
    
    # Get expenses by type
    expense_by_type = expenses.values('expense_type').annotate(
        total=Sum('amount'),
        count=Count('id')
    ).order_by('-total')
    
    # Prepare data for charts
    income_types = [i['income_type'] for i in income_by_type]
    income_amounts = [float(i['total']) for i in income_by_type]
    
    expense_types = [e['expense_type'] for e in expense_by_type]
    expense_amounts = [float(e['total']) for e in expense_by_type]
    
    context = {
        'income_total': income_total,
        'expense_total': expense_total,
        'profit': profit,
        'period': period,
        'period_name': period_name,
        'date_from': date_from.strftime('%Y-%m-%d') if date_from else '',
        'date_to': date_to.strftime('%Y-%m-%d') if date_to else '',
        'income_by_type': income_by_type,
        'expense_by_type': expense_by_type,
        'income_types': json.dumps(income_types),
        'income_amounts': json.dumps(income_amounts),
        'expense_types': json.dumps(expense_types),
        'expense_amounts': json.dumps(expense_amounts),
    }
    
    return render(request, 'accountant/report.html', context)

def expensesrecords(request):
    return render(request, 'accountant/expenses-records.html')

def incomerecords(request):
    return render(request, 'accountant/income-records.html')