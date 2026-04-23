from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['amount', 'currency', 'type', 'category', 'budget', 'user', 'occurred_at', 'created_at']
    list_filter = ['type', 'currency', 'created_at', 'occurred_at']
    search_fields = ['note', 'category__name', 'budget__name', 'user__email']
    date_hierarchy = 'occurred_at'
