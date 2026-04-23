from django.db import models
from django.conf import settings
import uuid


class Transaction(models.Model):
    """Transaction model for tracking income/expenses"""
    TYPE_CHOICES = [
        ('expense', 'Expense'),
        ('income', 'Income'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    budget = models.ForeignKey(
        'budgets.Budget',
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    category = models.ForeignKey(
        'categories.Category',
        on_delete=models.SET_NULL,
        null=True,
        related_name='transactions'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='transactions'
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='expense')
    currency = models.CharField(max_length=3, default='RUB')
    note = models.TextField(blank=True)
    occurred_at = models.DateTimeField()  # When transaction actually happened
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'transactions'
        ordering = ['-occurred_at']
        indexes = [
            models.Index(fields=['-occurred_at']),
            models.Index(fields=['budget', '-occurred_at']),
            models.Index(fields=['category', '-occurred_at']),
        ]

    def clean(self):
        """Validate that category belongs to the same budget as the transaction"""
        from django.core.exceptions import ValidationError
        if self.category and self.budget:
            if self.category.budget_id != self.budget_id:
                raise ValidationError({
                    'category': 'Category must belong to the same budget as the transaction'
                })

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.amount} {self.currency} - {self.category.name if self.category else 'No Category'}"
