import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from transactions.models import Transaction

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user(db):
    def make_user(**kwargs):
        return User.objects.create_user(
            email=kwargs.get("email", "user@example.com"),
            password=kwargs.get("password", "password123"),
            name=kwargs.get("name", "Test User")
        )
    return make_user

@pytest.fixture
def auth_client(api_client, create_user):
    user = create_user()
    response = api_client.post('http://localhost:8000/api/v1/auth/login/', {
        'email': 'user@example.com',
        'password': 'password123'
    }, format='json')
    print(response.json())
    token = response.data['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client, user


@pytest.mark.django_db
def test_create_transaction(auth_client):
    client, user = auth_client
    payload = {
        "amount": "250.00",
        "transaction_type": "deposit",
        "description": "Savings"
    }
    response = client.post("http://localhost:8000/api/v1/transactions/", payload, format='json')
    assert response.status_code == 201
    assert Transaction.objects.filter(user=user).count() == 1
    transaction = Transaction.objects.get(user=user)
    assert transaction.amount == 250.00
    assert transaction.transaction_type == "deposit"


@pytest.mark.django_db
def test_get_user_transactions(auth_client):
    client, user = auth_client
    Transaction.objects.create(user=user, amount=100, transaction_type='withdrawal')
    Transaction.objects.create(user=user, amount=300, transaction_type='deposit')

    response = client.get("http://localhost:8000/api/v1/transactions/")
    assert response.status_code == 200
    data = response.data
    assert len(data) == 2
    assert all(t["transaction_type"] in ["withdrawal", "deposit"] for t in data)


@pytest.mark.django_db
def test_transaction_requires_auth(api_client):
    payload = {
        "amount": "250.00",
        "transaction_type": "deposit",
        "description": "Unauthorized test"
    }
    response = api_client.post("http://localhost:8000/api/v1/transactions/", payload, format='json')
    assert response.status_code == 401


@pytest.mark.django_db
def test_cannot_create_invalid_transaction(auth_client):
    client, _ = auth_client
    invalid_payload = {
        "amount": "",  
        "transaction_type": "invalid_type",  
    }
    response = client.post("http://localhost:8000/api/v1/transactions/", invalid_payload, format='json')
    assert response.status_code == 400
    assert "amount" in response.data
    assert "transaction_type" in response.data
