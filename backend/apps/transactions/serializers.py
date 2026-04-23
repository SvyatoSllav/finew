from rest_framework import serializers
from .models import Transaction
from apps.categories.serializers import CategorySerializer
from apps.users.serializers import UserSerializer


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for Transaction"""
    category_detail = CategorySerializer(source='category', read_only=True)
    user_detail = UserSerializer(source='user', read_only=True)

    class Meta:
        model = Transaction
        fields = [
            'id', 'budget', 'category', 'category_detail', 'user', 'user_detail',
            'amount', 'type', 'currency', 'note', 'occurred_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Set user from request
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
