from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.paginator import Paginator
from .models import ExpenseIncome
from .serializers import ExpenseIncomeSerializer, ExpenseIncomeListSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_expenses(request):
    # List all expenses/income for the authenticated user with pagination
    user = request.user
    
    
    if user.is_superuser:
        expenses = ExpenseIncome.objects.all()
    else:
        expenses = ExpenseIncome.objects.filter(user=user)
    
    # Handle pagination
    page_size = request.query_params.get('page_size', 10)
    page_number = request.query_params.get('page', 1)
    
    try:
        page_size = int(page_size)
        page_number = int(page_number)
    except ValueError:
        return JsonResponse({'error': 'Invalid page parameters'}, status=HTTP_400_BAD_REQUEST)
    
    paginator = Paginator(expenses, page_size)
    
    try:
        page_obj = paginator.get_page(page_number)
    except:
        return JsonResponse({'error': 'Invalid page number'}, status=HTTP_400_BAD_REQUEST)
    
    serializer = ExpenseIncomeListSerializer(page_obj, many=True)
    
    # Build pagination response
    response_data = {
        'count': paginator.count,
        'next': f"?page={page_obj.next_page_number()}" if page_obj.has_next() else None,
        'previous': f"?page={page_obj.previous_page_number()}" if page_obj.has_previous() else None,
        'results': serializer.data
    }
    
    return Response(response_data, status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_expense(request):
    """Create a new expense/income record"""
    serializer = ExpenseIncomeSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save(user=request.user)
        return JsonResponse({**serializer.data, 'message': 'Expense/Income created successfully', 'status': HTTP_201_CREATED})
    return JsonResponse(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_expense_by_id(request, id):
    #Geting a specific expense/income record by ID
    try:
        user = request.user
        if user.is_superuser:
            expense = ExpenseIncome.objects.get(pk=id)
        else:
            expense = ExpenseIncome.objects.get(pk=id, user=user)
        
        serializer = ExpenseIncomeSerializer(expense)
        return Response(serializer.data, status=HTTP_200_OK)
    
    except ExpenseIncome.DoesNotExist:
        return JsonResponse({'error': 'Expense/Income record not found'}, status=HTTP_403_FORBIDDEN)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_expense(request, id):
    #Update a specific expense/income record
    try:
        user = request.user
        if user.is_superuser:
            expense = ExpenseIncome.objects.get(pk=id)
        else:
            expense = ExpenseIncome.objects.get(pk=id, user=user)
        
        serializer = ExpenseIncomeSerializer(expense, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({**serializer.data, 'message': 'Expense/Income updated successfully', 'status': HTTP_200_OK})
        return JsonResponse(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    except ExpenseIncome.DoesNotExist:
        return JsonResponse({'error': 'Expense/Income record not found'}, status=HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_expense(request, id):
    try:
        user = request.user
        if user.is_superuser:
            expense = ExpenseIncome.objects.get(pk=id)
        else:
            expense = ExpenseIncome.objects.get(pk=id, user=user)
        
        expense.delete()
        return Response({'message': 'Expense/Income deleted successfully'}, status=HTTP_204_NO_CONTENT)
    
    except ExpenseIncome.DoesNotExist:
        return JsonResponse({'error': 'Expense/Income record not found'}, status=HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_expenses_by_type(request):
    transaction_type = request.query_params.get('type')
    valid_types = ['credit', 'debit']
    user = request.user
    
    if transaction_type:
        if transaction_type not in valid_types:
            return JsonResponse({'error': 'Invalid transaction type specified'}, status=HTTP_400_BAD_REQUEST)
        
        if user.is_superuser:
            expenses = ExpenseIncome.objects.filter(transaction_type=transaction_type)
        else:
            expenses = ExpenseIncome.objects.filter(transaction_type=transaction_type, user=user)
    else:
        if user.is_superuser:
            expenses = ExpenseIncome.objects.all()
        else:
            expenses = ExpenseIncome.objects.filter(user=user)
    
    serializer = ExpenseIncomeListSerializer(expenses[:20], many=True)
    return Response(serializer.data, status=HTTP_200_OK)


