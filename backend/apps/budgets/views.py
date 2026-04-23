from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Budget, BudgetMember, BudgetInvite
from .serializers import (
    BudgetSerializer,
    BudgetMemberSerializer,
    BudgetInviteSerializer,
    JoinBudgetSerializer
)
from .permissions import IsBudgetMember, IsBudgetOwnerOrEditor, IsBudgetOwner


class BudgetViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Budget CRUD operations
    """
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return budgets where user is a member
        return Budget.objects.filter(members=self.request.user).distinct()

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), IsBudgetOwnerOrEditor()]
        elif self.action == 'destroy':
            return [IsAuthenticated(), IsBudgetOwner()]
        return super().get_permissions()

    def perform_create(self, serializer):
        # Set author to current user
        budget = serializer.save(author=self.request.user)

        # Add creator as owner
        BudgetMember.objects.create(
            budget=budget,
            user=self.request.user,
            role='owner'
        )

    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """Get list of budget members"""
        budget = self.get_object()
        members = budget.budget_members.all()
        serializer = BudgetMemberSerializer(members, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def invites(self, request, pk=None):
        """Generate invite code for budget"""
        budget = self.get_object()

        # Check if user is owner or editor
        member = budget.budget_members.filter(user=request.user).first()
        if not member or member.role not in ['owner', 'editor']:
            return Response(
                {'error': 'Only owners and editors can create invites'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Create invite
        invite = BudgetInvite.objects.create(
            budget=budget,
            invited_by=request.user
        )

        serializer = BudgetInviteSerializer(invite)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def join(self, request):
        """Join budget via invite code or budget ID"""
        serializer = JoinBudgetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data.get('code')
        budget_id = serializer.validated_data.get('budget_id')

        if code:
            # Join via invite code
            try:
                invite = BudgetInvite.objects.get(code=code)
                if not invite.is_valid():
                    return Response(
                        {'error': 'Invite code is expired or already used'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                budget = invite.budget
                invite.used_by = request.user
                invite.save()
            except BudgetInvite.DoesNotExist:
                return Response(
                    {'error': 'Invalid invite code'},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            # Join via budget ID (for backward compatibility with old sharing method)
            try:
                budget = Budget.objects.get(id=budget_id)
            except Budget.DoesNotExist:
                return Response(
                    {'error': 'Budget not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

        # Check if user is already a member
        if budget.members.filter(id=request.user.id).exists():
            return Response(
                {'error': 'You are already a member of this budget'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Add user as viewer
        BudgetMember.objects.create(
            budget=budget,
            user=request.user,
            role='viewer'
        )

        serializer = BudgetSerializer(budget)
        return Response(serializer.data, status=status.HTTP_200_OK)
