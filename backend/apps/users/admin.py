from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'display_name', 'auth_provider', 'is_staff', 'created_at']
    list_filter = ['auth_provider', 'is_staff', 'is_active']
    search_fields = ['email', 'display_name']
    ordering = ['-created_at']

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('uid', 'display_name', 'avatar_url', 'default_budget', 'auth_provider', 'provider_uid')
        }),
    )

    readonly_fields = ['uid', 'created_at', 'updated_at']
