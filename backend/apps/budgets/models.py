from django.db import models
from django.conf import settings
import uuid
from datetime import timedelta
from django.utils import timezone
import secrets


class Budget(models.Model):
    """Budget model representing a shared budget"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    currency = models.CharField(max_length=3, default='RUB')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='authored_budgets'
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='BudgetMember',
        related_name='budgets'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'budgets'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.author.email})"


class BudgetMember(models.Model):
    """Through model for Budget-User many-to-many relationship"""
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('editor', 'Editor'),
        ('viewer', 'Viewer'),
    ]

    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='budget_members')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='viewer')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'budget_members'
        unique_together = ['budget', 'user']

    def __str__(self):
        return f"{self.user.email} - {self.budget.name} ({self.role})"


class BudgetInvite(models.Model):
    """Budget invite codes for sharing"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='invites')
    invited_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=32, unique=True)
    expires_at = models.DateTimeField()
    used_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='used_invites'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'budget_invites'

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = secrets.token_urlsafe(16)
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(days=7)
        super().save(*args, **kwargs)

    def is_valid(self):
        return self.used_by is None and self.expires_at > timezone.now()

    def __str__(self):
        return f"Invite for {self.budget.name} by {self.invited_by.email}"
