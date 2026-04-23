from rest_framework import serializers
from .models import Budget, BudgetMember, BudgetInvite
from apps.users.serializers import UserSerializer


class BudgetMemberSerializer(serializers.ModelSerializer):
    """Serializer for BudgetMember"""
    user = UserSerializer(read_only=True)

    class Meta:
        model = BudgetMember
        fields = ['user', 'role', 'joined_at']


class BudgetSerializer(serializers.ModelSerializer):
    """Serializer for Budget"""
    author = UserSerializer(read_only=True)
    budget_members = BudgetMemberSerializer(many=True, read_only=True, source='budgetmember_set')

    class Meta:
        model = Budget
        fields = ['id', 'name', 'currency', 'author', 'budget_members', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Author is set from request.user in the view
        return super().create(validated_data)


class BudgetInviteSerializer(serializers.ModelSerializer):
    """Serializer for BudgetInvite"""
    budget_name = serializers.CharField(source='budget.name', read_only=True)
    invited_by_email = serializers.EmailField(source='invited_by.email', read_only=True)

    class Meta:
        model = BudgetInvite
        fields = ['id', 'budget', 'budget_name', 'invited_by', 'invited_by_email', 'code', 'expires_at', 'used_by', 'created_at']
        read_only_fields = ['id', 'code', 'invited_by', 'created_at']


class JoinBudgetSerializer(serializers.Serializer):
    """Serializer for joining a budget via code or ID"""
    code = serializers.CharField(required=False)
    budget_id = serializers.UUIDField(required=False)

    def validate(self, data):
        if not data.get('code') and not data.get('budget_id'):
            raise serializers.ValidationError('Either code or budget_id must be provided')
        return data
