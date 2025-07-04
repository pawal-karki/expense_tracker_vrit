from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class ExpenseIncome(models.Model):
    TRANSACTION_TYPES = [
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    ]
    
    TAX_TYPES = [
        ('flat', 'Flat'),
        ('percentage', 'Percentage'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    tax_type = models.CharField(max_length=15, choices=TAX_TYPES, default='flat')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.amount} ({self.transaction_type})"
    
    @property
    def total(self):
        """Calculate total amount including tax"""
        if self.tax_type == 'percentage':
            # Percentage tax: Total = Amount + (Amount × Tax ÷ 100)
            tax_amount = self.amount * (self.tax / Decimal('100'))
            return self.amount + tax_amount
        else:
            # Flat tax: Total = Amount + Tax
            return self.amount + self.tax
