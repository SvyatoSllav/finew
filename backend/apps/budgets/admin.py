from django.contrib import admin
from .models import Budget, BudgetMember, BudgetInvite


class BudgetMemberInline(admin.TabularInline):
    model = BudgetMember
    extra = 1


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'currency', 'created_at']
    list_filter = ['currency', 'created_at']
    search_fields = ['name', 'author__email']
    inlines = [BudgetMemberInline]


@admin.register(BudgetMember)
class BudgetMemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'budget', 'role', 'joined_at']
    list_filter = ['role', 'joined_at']
    search_fields = ['user__email', 'budget__name']


@admin.register(BudgetInvite)
class BudgetInviteAdmin(admin.ModelAdmin):
    list_display = ['budget', 'invited_by', 'code', 'expires_at', 'used_by', 'created_at']
    list_filter = ['created_at', 'expires_at']
    search_fields = ['code', 'budget__name', 'invited_by__email']
    readonly_fields = ['code']
