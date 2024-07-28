# api/views.py
from django.http import HttpResponse
from decimal import Decimal
import csv
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Expense, Share
from .serializers import UserSerializer, ExpenseSerializer, ShareSerializer

@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def retrieve_user_details(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['POST'])
def add_expense(request):
    serializer = ExpenseSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def retrieve_individual_expenses(request, user_id):
    expenses = Expense.objects.filter(creator_id=user_id)
    serializer = ExpenseSerializer(expenses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def retrieve_overall_expenses(request):
    expenses = Expense.objects.all()
    serializer = ExpenseSerializer(expenses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def download_balance_sheet(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="balance_sheet.csv"'
    writer = csv.writer(response)
    
    # Fetch expenses and related data efficiently
    expenses = Expense.objects.all().prefetch_related('shares__user')
    users = User.objects.all().prefetch_related('created_expenses', 'shared_expenses')
    
    # Individual expenses
    writer.writerow(['Expense ID', 'Expense Title', 'Total Amount', 'User ID', 'User Name', 'Share Type', 'Amount Per Share'])
    for expense in expenses:
        for share in expense.shares.all():
            share_amount = share.amount if share.amount is not None else Decimal('0.00')
            writer.writerow([
                expense.id,
                expense.title,
                expense.total_amount,
                share.user.id,
                share.user.name,
                share.share_type,
                share_amount
            ])
    
    # Overall and due amounts
    writer.writerow([])
    writer.writerow(['User ID', 'User Name', 'Total Amount Owed', 'Total Amount Due'])
    for user in users:
        total_paid = sum(expense.total_amount for expense in user.created_expenses.all())
        total_owed = sum(share.amount or Decimal('0.00') for share in user.shared_expenses.all())
        amount_due = total_owed - total_paid
        writer.writerow([user.id, user.name, total_owed, amount_due])

    return response