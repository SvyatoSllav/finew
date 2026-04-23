from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['uid', 'email', 'display_name', 'avatar_url', 'default_budget', 'auth_provider', 'created_at']
        read_only_fields = ['uid', 'created_at', 'auth_provider']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['email', 'password', 'display_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            display_name=validated_data.get('display_name', ''),
            auth_provider='email'
        )
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})


class GoogleAuthSerializer(serializers.Serializer):
    """Serializer for Google OAuth authentication"""
    token = serializers.CharField(write_only=True)

    def validate_token(self, token):
        """Verify Google ID token"""
        try:
            # Verify the token with Google
            idinfo = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                # You'll need to set GOOGLE_CLIENT_ID in settings
                getattr(settings, 'GOOGLE_CLIENT_ID', None)
            )

            # Token is valid, return user info
            return {
                'email': idinfo.get('email'),
                'display_name': idinfo.get('name', ''),
                'avatar_url': idinfo.get('picture', ''),
                'provider_uid': idinfo.get('sub'),
            }
        except ValueError as e:
            raise serializers.ValidationError(f'Invalid Google token: {str(e)}')

    def create(self, validated_data):
        """Create or retrieve user from Google auth"""
        token_data = validated_data['token']

        # Try to find user by email or provider_uid
        user = User.objects.filter(
            email=token_data['email']
        ).first()

        if user:
            # Update user info from Google if provider is Google
            if user.auth_provider == 'google':
                user.display_name = token_data.get('display_name', user.display_name)
                user.avatar_url = token_data.get('avatar_url', user.avatar_url)
                user.save()
        else:
            # Create new user
            user = User.objects.create_user(
                username=token_data['email'],
                email=token_data['email'],
                display_name=token_data.get('display_name', ''),
                avatar_url=token_data.get('avatar_url', ''),
                auth_provider='google',
                provider_uid=token_data.get('provider_uid', ''),
                password=None  # No password for OAuth users
            )
            user.set_unusable_password()
            user.save()

        return user


class TokenSerializer(serializers.Serializer):
    """Serializer for JWT tokens"""
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)


def get_tokens_for_user(user):
    """Generate JWT tokens for user"""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
