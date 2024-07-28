# api/serializers.py
from decimal import Decimal
from rest_framework import serializers
from .models import User, Expense, Share
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    name = serializers.CharField(required=True, max_length=100)
    mobile = serializers.CharField(required=True, max_length=15)

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'mobile']

    def validate_email(self, value):
        # Validate email format
        email_validator = EmailValidator()
        try:
            email_validator(value)
        except ValidationError as e:
            raise serializers.ValidationError("Invalid email format.") from e
        
        # Check for email uniqueness
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        
        return value
    def validate_mobile(self, value):
        if User.objects.filter(mobile=value).exists():
            raise serializers.ValidationError("This mobile number is already in use.")
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError("Mobile number must be 10 digits.")
        return value

class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Share
        fields = ['user', 'amount', 'share_type', 'percentage']

class ExpenseSerializer(serializers.ModelSerializer):
    shares = ShareSerializer(many=True)

    class Meta:
        model = Expense
        fields = ['id', 'title', 'total_amount', 'creator', 'created_at', 'shares']

    def validate(self, data):
        shares = data.get('shares', [])
        total_amount = data.get('total_amount')

        # Validate sums and distributions based on share type
        exact_sum_shares = sum(Decimal(share['amount']) for share in shares if share.get('share_type') == 'exact')
        if any(share.get('share_type') == 'exact' for share in shares) and exact_sum_shares != total_amount:
            raise serializers.ValidationError("The sum of the exact shares must equal the total amount of the expense.")

        if any(share.get('share_type') == 'percentage' for share in shares):
            total_percentage = sum(Decimal(share.get('percentage', 0)) for share in shares if share.get('share_type') == 'percentage')
            if total_percentage != Decimal('100'):
                raise serializers.ValidationError("Total percentages must sum up to 100%.")

        if any(share.get('share_type') == 'equal' for share in shares) and any('amount' in share for share in shares if share.get('share_type') == 'equal'):
            raise serializers.ValidationError("No amounts should be provided for 'equal' share type, it will be calculated automatically.")

        return data

    def create(self, validated_data):
        shares_data = validated_data.pop('shares', [])
        expense = Expense.objects.create(**validated_data)
        total_amount = validated_data['total_amount']

        # Recalculate equal shares if applicable
        equal_shares = [share for share in shares_data if share.get('share_type') == 'equal']
        if equal_shares:
            equal_amount = total_amount / len(equal_shares)
            for share in equal_shares:
                share['amount'] = equal_amount

        for share_data in shares_data:
            if share_data.get('share_type') == 'percentage':
                share_data['amount'] = (Decimal(share_data['percentage']) / Decimal('100')) * Decimal(total_amount)
            Share.objects.create(expense=expense, **share_data)

        return expense