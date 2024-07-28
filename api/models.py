# api/models.py

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class User(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)

class Expense(models.Model):
    title = models.CharField(max_length=255)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    creator = models.ForeignKey(User, related_name='created_expenses', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Share(models.Model):
    expense = models.ForeignKey(Expense, related_name='shares', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='shared_expenses', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    share_type = models.CharField(max_length=10, choices=[('equal', 'Equal'), ('exact', 'Exact'), ('percentage', 'Percentage')])
    percentage = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=True)