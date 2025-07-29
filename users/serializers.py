from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate


# Connect and serialize CustomUser model from users/models.py to register new users
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'password')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user


# Login users using the djangos built-in authentication system, the authenticate() function uses the AUTHENTICATION_BACKENDS in settings.py to determine how to authenticate the user.
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("invalid credentials")
        if not user.is_active:
            raise serializers.ValidationError("This account is currently inactive. This could be due to pending verification, suspension, or deactivation. For assistance, contact support.")
        return {'user': user}