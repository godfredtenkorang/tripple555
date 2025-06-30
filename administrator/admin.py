from django.contrib import admin
from .models import Battery, StockHistory

# Register your models here.
admin.site.register(Battery)
admin.site.register(StockHistory)