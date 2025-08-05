import pytest
from rest_framework.test import APIClient
from users.models import CustomUser
from django.core import mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator

@pytest.mark.django_db
class TestUserAuth:
    def setup_method(self):
        """Runs before every test method."""
        self.client = APIClient()
        self.register_url = 'http://localhost:8000/api/v1/users/register/'
        self.login_url = 'http://localhost:8000/api/v1/users/login/'
        self.logout_url = 'http://localhost:8000/api/v1/users/logout/'
        self.reset_request_url = 'http://localhost:8000/api/v1/users/reset-password/'

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

    def test_password_reset(self):
        """Test that requesting a password reset sends an email."""
        user = CustomUser.objects.create_user(
            email="resetuser@example.com",
            name="Reset User",
            password="OldPass123"
        )

        response = self.client.post(
            self.reset_request_url,
            {"email": user.email},
            format="json"
        )

        assert response.status_code == 200
        assert "Password reset link has been sent to your email." in str(response.data)
        assert len(response.data) == 1
        assert user.email in mail.outbox[0].to

    
    def test_password_reset_confirm_changes_password(self):
        """Test that a reset link allows changing the password."""
        user = CustomUser.objects.create_user(
            email="confirmreset@example.com",
            name="Reset Confirm",
            password="OldPassword123"
        )

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)
        confirm_url = f"/api/v1/users/reset-password-confirm/{uid}/{token}/"

        new_password = "NewPassword456"
        response = self.client.post(confirm_url, {"new_password": new_password}, format='json')

        assert response.status_code == 200
        assert "Password reset successful." in str(response.data)

        login_response = self.client.post(self.login_url, {
            "email": user.email, "password": "OldPassword123"}, format='json')
        
        assert login_response.status_code == 400

        login_response = self.client.post(self.login_url, {"email": user.email, "password": new_password}, format='json')
        assert login_response.status_code == 200
        assert 'access' in login_response.data