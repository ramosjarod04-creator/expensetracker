# tracker/models.py
from django.db import models
# Tinanggal ang: from django.contrib.auth.models import User 

class Expense(models.Model):
    # Walang user field dito
    
    # Mga choices para sa Category field
    CATEGORY_CHOICES = [
        ('food', 'Food & Dining'),
        ('transport', 'Transportation'),
        ('shopping', 'Shopping'),
        ('bills', 'Bills & Utilities'),
        ('entertainment', 'Entertainment'),
        ('other', 'Other'),
    ]

    date = models.DateField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2) # Para sa PHP

    def __str__(self):
        return f"{self.date} - {self.description} ({self.amount})"