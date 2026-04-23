from django.db import models
import uuid


class Category(models.Model):
    """Category model for organizing transactions"""
    TYPE_CHOICES = [
        ('expense', 'Expense'),
        ('income', 'Income'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    budget = models.ForeignKey(
        'budgets.Budget',
        on_delete=models.CASCADE,
        related_name='categories'
    )
    name = models.CharField(max_length=255)
    icon_name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default='#000000')  # Hex color
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='expense')
    sort_order = models.IntegerField(default=0)
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'categories'
        ordering = ['sort_order', 'name']
        unique_together = ['budget', 'name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f"{self.name} ({self.budget.name})"
