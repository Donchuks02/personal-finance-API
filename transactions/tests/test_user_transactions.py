import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from transactions.models import Category, SubAccount
from pprint import pprint


User = get_user_model()


@pytest.mark.django_db
class TestSubAccountSetup:

    def test_user_auto_accounts_created(self):
        """
        Test that sub-accounts(Income and Expenses) are automatically created for a user upon registration with default categories.
        """
        user = User.objects.create_user(email="testuser@example.com", password="testpassword123")
        accounts = SubAccount.objects.filter(user=user)
        assert accounts.count() == 2

        income = accounts.filter(account_type="income")
        expenses = accounts.filter(account_type="expense")

        assert income is not None
        assert expenses is not None

        # check if default categories is created alongside
        default_categories = Category.objects.filter(sub_account__in=expenses)
        # print(default_categories)
        assert default_categories.count() >= 10
        assert "Food" in default_categories.values_list("name", flat=True)






@pytest.mark.django_db
class TestAPIEndpoints:

    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email="testuser@example.com", password="testpassword123")
        self.client.force_authenticate(self.user)

    def test_list_sub_accounts(self):
        """
        Authenticated user should be able to list their sub_accounts.
        """
        response = self.client.get("/api/v1/transactions/sub_accounts/")
        assert response.status_code == 200
        data = response.json()
        pprint(data)
        
       
        assert any(acc["account_type"] == "income" for acc in data)
        assert any(acc["account_type"] == "expense" for acc in data)


    def test_list_categories_under_expenses(self):
        """
        Should return predefined categories for expenses account.
        """
        expenses_account = SubAccount.objects.get(user=self.user, account_type="expense")

        response = self.client.get(f"/api/v1/transactions/sub_accounts/{expenses_account.id}/categories/")
        assert response.status_code == 200
        data = response.json()
        assert "Food" in [cat["name"] for cat in data]