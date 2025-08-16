from django.shortcuts import render
from .models import Transaction, SubAccount, Category
from .serializers import TransactionSerializer
from rest_framework import generics, permissions


class TransactionListCreateView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(account__user=self.request.user).order_by("-created_at")
    
    def perform_create(self, serializer):
        serializer.save()

class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(account__user=self.request.user)