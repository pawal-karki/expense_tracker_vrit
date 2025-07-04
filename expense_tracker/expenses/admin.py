from django.contrib import admin
from .models import ExpenseIncome


@admin.register(ExpenseIncome)
class ExpenseIncomeAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'amount', 'transaction_type', 'tax', 'tax_type', 'total', 'created_at']
    list_filter = ['transaction_type', 'tax_type', 'created_at', 'user']
    search_fields = ['title', 'description', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def total(self, obj):
        return obj.total
    total.short_description = 'Total Amount'
