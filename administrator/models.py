from django.db import models
from users.models import User

# Create your models here.
from django.core.validators import MinValueValidator

class Battery(models.Model):
    BATTERY_TYPES = (
        ('lead_acid', 'Lead Acid'),
        ('agm', 'AGM'),
        ('gel', 'Gel'),
        ('lithium', 'Lithium'),
    )
    
    name = models.CharField(max_length=100)
    battery_type = models.CharField(max_length=20, choices=BATTERY_TYPES)
    capacity = models.CharField(max_length=20)  # e.g., "12V 60Ah"
    quantity = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    min_stock_level = models.PositiveIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.capacity})"
    
    @property
    def is_low_stock(self):
        return self.quantity <= self.min_stock_level
    
    @property
    def total_value(self):
        return self.quantity * self.unit_cost
    
    def __str__(self):
        return self.name

class StockHistory(models.Model):
    battery = models.ForeignKey(Battery, on_delete=models.CASCADE)
    quantity_change = models.IntegerField()  # Positive for addition, negative for sales
    new_quantity = models.PositiveIntegerField()
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.battery