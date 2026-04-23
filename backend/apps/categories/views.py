from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category
from .serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Category CRUD operations
    """
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['budget', 'type', 'is_archived']
    ordering_fields = ['sort_order', 'name', 'created_at']
    ordering = ['sort_order', 'name']

    def get_queryset(self):
        # Return categories for budgets where user is a member
        return Category.objects.filter(budget__members=self.request.user)
