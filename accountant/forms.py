from django import forms
from .models import Income, Expense
from administrator.models import Battery

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['income_type', 'battery', 'amount', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show batteries that are in stock
        self.fields['battery'].queryset = Battery.objects.filter(quantity__gt=0)

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['expense_type', 'amount', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }