from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class User(AbstractUser):
    """Custom user model extending Django's AbstractUser"""
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    email = models.EmailField(unique=True)
    display_name = models.CharField(max_length=255, blank=True)
    avatar_url = models.URLField(blank=True, null=True)
    # Removed default_budget to avoid circular dependency
    # Frontend can determine default budget by querying budgets with role='owner'
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # OAuth provider info
    auth_provider = models.CharField(
        max_length=50,
        choices=[('email', 'Email'), ('google', 'Google')],
        default='email'
    )
    provider_uid = models.CharField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email
