from django.urls import path
from .views import TransactionViewSet, SubAccountViewSet, CategoryViewSet
from rest_framework.routers import DefaultRouter


# Create a router and register the viewsets
router = DefaultRouter()
router.register(r"sub_accounts", SubAccountViewSet, basename='subaccount')
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"transactions", TransactionViewSet, basename="transaction")

urlpatterns = router.urls