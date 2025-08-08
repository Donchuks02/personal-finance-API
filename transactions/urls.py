from django.urls import path
from .views import TransactionListCreateView, TransactionDetailView


urlpatterns = [
    path('', TransactionListCreateView.as_view(), name='create_transaction_list'),
    path('<int:pk>/', TransactionDetailView.as_view(), name='transaction_detail'),
]