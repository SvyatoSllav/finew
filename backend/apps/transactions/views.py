from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Transaction
from .serializers import TransactionSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Transaction CRUD operations
    """
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['budget', 'category', 'type', 'currency']
    ordering_fields = ['occurred_at', 'amount', 'created_at']
    ordering = ['-occurred_at']

    def get_queryset(self):
        # Return transactions for budgets where user is a member
        return Transaction.objects.filter(
            budget__members=self.request.user
        ).select_related('category', 'user', 'budget')
