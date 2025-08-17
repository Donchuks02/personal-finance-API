from rest_framework import serializers
from .models import Transaction, SubAccount, Category


class SubAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubAccount
        fields = ['id', 'account_type', 'balance']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["id", "sub_account", "transaction_type", "amount", "description", "created_at"]
        read_only_fields = ["id", "created_at"]


    def validate(self, data):
        request = self.context.get('request')
        if data["sub_account"].user != request.user:
            raise serializers.ValidationError("You cannot add transactions to accounts that are not yours.")