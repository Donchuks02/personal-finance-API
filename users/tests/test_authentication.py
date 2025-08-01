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
        self.logout_url = 'http://localhost:8000/api/v1/users/logout/'

    def test_user_registration_success(self):
        """Test successful user registration."""
        payload = {
            "email": "VonUser@gmail.com",
            "name": "Von",
            "password": "Von12345",
        }
        response = self.client.post(self.register_url, payload, format='json')


        assert response.status_code == 201
        assert CustomUser.objects.filter(email=payload['email']).exists()

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

    def test_user_logout(self):
        """Test the users logout funtionality."""
        CustomUser.objects.create_user(
            email="logoutVon@gmail.com",
            name="Von",
            password="VonPassword123"
        )
        payload = {
            "email": "logoutVon@gmail.com",
            "password": "VonPassword123"
        }


        login_response = self.client.post(self.login_url, payload, format='json')
        assert login_response.status_code == 200
        refresh_token = login_response.data['refresh']
        access_token = login_response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        logout_response = self.client.post(self.logout_url, {"refresh": refresh_token}, format='json')
        # print(logout_response.data)
        assert logout_response.status_code == 205
        assert 'Successfully logged out.' in str(logout_response.data)