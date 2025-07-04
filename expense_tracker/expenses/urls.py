from django.urls import path
from .views import (
    get_expenses,
    create_expense,
    get_expense_by_id,
    update_expense,
    delete_expense,
    get_expenses_by_type,
    
)

urlpatterns = [
    path('expenses/', get_expenses, name='get_expenses'),
    path('expenses/create/', create_expense, name='create_expense'),
    path('expenses/<int:id>/', get_expense_by_id, name='get_expense_by_id'),
    path('expenses/<int:id>/update/', update_expense, name='update_expense'),
    path('expenses/<int:id>/delete/', delete_expense, name='delete_expense'),
    path('expenses/by-type/', get_expenses_by_type, name='get_expenses_by_type'), #optional test
] 