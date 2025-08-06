from rest_framework import serializers
from .models import Transaction



class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["id", "user", "amount", "transaction_type", "category", "description", "date", "created_at"]
        read_only_fields = ["id", "user", "created_at"]

    # This methodmakes sure that each transaction is connected to the user who created it automatically
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)