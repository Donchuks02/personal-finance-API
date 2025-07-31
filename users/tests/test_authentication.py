import pytest
from rest_framework.test import APIClient
from users.models import CustomUser

@pytest.mark.django_db
class TestUserAuth:
    def setup_method(self):
        """Runs before every test method."""
        self.client = APIClient()
        self.register_url = 'http://localhost:8000/api/v1/users/register/'
        self.login_url = 'http://localhost:8000/api/v1/users/login/'

    def test_user_registration_success(self):
        """Test successful user registration."""
        payload = {
            "email": "VonUser@gmail.com",
            "name": "Von",
            "password": "Von12345",
        }
        response = self.client.post(self.register_url, payload, format='json')

        # verify expected response
        assert response.status_code == 201

        # verify that user is created in the database
        assert CustomUser.objects.filter(email=payload['email']).exists()

        # Check if the response contains the expected data
        data = response.json()
        assert data['email'] == payload['email']
        assert data['name'] == payload['name']

    def test_user_login_success(self):
        """Test that login after registration returns a  JWT token"""
        user = CustomUser.objects.create_user(
            email="loginVon@gmail.com",
            name="Von",
            password="VonPassword123"
        )
        payload = {
            "email": "loginVon@gmail.com",
            "password": "VonPassword123"
        }

        response = self.client.post(self.login_url, payload, format='json')
        assert response.status_code == 200
        data = response.json()
        assert "access" in data
        assert "refresh" in data
        assert data['user']['email'] == user.email

    def test_user_login_invalid_credentials(self):
        """Test login fails with wrong password."""
        CustomUser.objects.create_user(
            email="wrongpass@example.com",
            name="Wrong Pass",
            password="CorrectPassword123"
        )

        payload = {
            "email": "wrongpass@example.com",
            "password": "WrongPassword"
        }
        response = self.client.post(self.login_url, payload, format='json')

        assert response.status_code == 400
        assert 'invalid credentials' in str(response.data)