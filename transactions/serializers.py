from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["id", "account", "transaction_type", "amount", "description", "created_at"]
        read_only_fields = ["id", "created_at"]


    def validate(self, data):
        request = self.context.get('request')
        if data["account"].user != request.user:
            raise serializers.ValidationError("You cannot add transactions to accounts that are not yours.")