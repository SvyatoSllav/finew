from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category"""
    class Meta:
        model = Category
        fields = ['id', 'budget', 'name', 'icon_name', 'color', 'type', 'sort_order', 'is_archived', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        # Check if category with same name exists in budget
        budget = data.get('budget')
        name = data.get('name')

        if budget and name:
            # For updates, exclude current instance
            queryset = Category.objects.filter(budget=budget, name=name)
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)

            if queryset.exists():
                raise serializers.ValidationError({'name': 'Category with this name already exists in this budget'})

        return data
