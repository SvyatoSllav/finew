from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'budget', 'type', 'icon_name', 'sort_order', 'is_archived', 'created_at']
    list_filter = ['type', 'is_archived', 'created_at']
    search_fields = ['name', 'budget__name']
    list_editable = ['sort_order', 'is_archived']
