from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Transaction
from .serializers import TransactionSerializer

# Create your views here.

class TransactionListCreateView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        queryset = Transaction.objects.filter(user=self.request.user)
        t_type = self.request.query_params.get('type')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if t_type:
            queryset = queryset.filter(transaction_type=t_type)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        return queryset
    
class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)