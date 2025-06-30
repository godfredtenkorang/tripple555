from django import forms
from .models import Battery

class BatteryForm(forms.ModelForm):
    class Meta:
        model = Battery
        fields = ['name', 'battery_type', 'capacity', 'quantity', 'unit_cost', 'min_stock_level']
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': 0}),
            'unit_cost': forms.NumberInput(attrs={'min': 0, 'step': '0.01'}),
            'min_stock_level': forms.NumberInput(attrs={'min': 0}),
        }