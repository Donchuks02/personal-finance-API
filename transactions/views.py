from django.shortcuts import render
from .models import Transaction, SubAccount, Category
from .serializers import TransactionSerializer, SubAccountSerializer, CategorySerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics, permissions, viewsets



class SubAccountViewSet(viewsets.ModelViewSet):
    serializer_class = SubAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SubAccount.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=["get"])
    def categories(self, request, pk=None):
        sub_account = self.get_object()
        categories = Category.objects.filter(sub_account=sub_account)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only transactions belonging to the authenticated user
        return Transaction.objects.filter(
            sub_account__user=self.request.user
        ).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save()