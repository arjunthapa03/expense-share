# tests.py or test_api.py under your Django app directory
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User, Expense, Share
from decimal import Decimal

class ExpenseShareTests(APITestCase):

    def setUp(self):
        # Set up initial data
        self.user1 = User.objects.create(email='alice@example.com', name='Alice', mobile='1234567890')
        self.user2 = User.objects.create(email='bob@example.com', name='Bob', mobile='1234567891')
        self.expense = Expense.objects.create(title='Lunch', total_amount=Decimal('60.00'), creator=self.user1)
        Share.objects.create(expense=self.expense, user=self.user1, amount=Decimal('30.00'), share_type='exact')
        Share.objects.create(expense=self.expense, user=self.user2, amount=Decimal('30.00'), share_type='exact')

    def test_create_user(self):
        """
        Ensure we can create a new user.
        """
        url = reverse('create_user')
        data = {'email': 'carol@example.com', 'name': 'Carol', 'mobile': '1234567892'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_user_details(self):
        """
        Ensure we can retrieve a user's details.
        """
        url = reverse('retrieve_user_details', args=[self.user1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'alice@example.com')

    def test_add_expense(self):
        """
        Ensure we can add an expense.
        """
        url = reverse('add_expense')
        data = {'title': 'Dinner', 'total_amount': '100.00', 'creator': self.user1.id,
                'shares': [{'user': self.user1.id, 'amount': '50.00', 'share_type': 'exact'},
                           {'user': self.user2.id, 'amount': '50.00', 'share_type': 'exact'}]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_individual_expenses(self):
        """
        Ensure we can retrieve individual expenses for a user.
        """
        url = reverse('retrieve_individual_expenses', args=[self.user1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_retrieve_overall_expenses(self):
        """
        Ensure we can retrieve all expenses.
        """
        url = reverse('retrieve_overall_expenses')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_download_balance_sheet(self):
        """
        Ensure we can download the balance sheet.
        """
        url = reverse('download_balance_sheet')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Use the .headers dictionary to access response headers
        self.assertIn('Content-Type', response.headers)
        self.assertEqual(response.headers['Content-Type'], 'text/csv')