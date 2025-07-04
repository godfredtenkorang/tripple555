from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLES = (
        ('ADMIN', 'Administrator'),
        ('ACCOUNTANT', 'Accountant'),
    )
    role = models.CharField(max_length=10, choices=ROLES)
    
    
    def __str__(self):
        return self.username