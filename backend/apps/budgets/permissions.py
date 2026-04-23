from rest_framework import permissions


class IsBudgetMember(permissions.BasePermission):
    """
    Permission to check if user is a member of the budget
    """
    def has_object_permission(self, request, view, obj):
        # Check if user is a member of the budget
        return obj.members.filter(id=request.user.id).exists()


class IsBudgetOwnerOrEditor(permissions.BasePermission):
    """
    Permission to check if user is owner or editor of the budget
    """
    def has_object_permission(self, request, view, obj):
        # Allow safe methods for all members
        if request.method in permissions.SAFE_METHODS:
            return obj.members.filter(id=request.user.id).exists()

        # For modifications, check if user is owner or editor
        member = obj.budget_members.filter(user=request.user).first()
        return member and member.role in ['owner', 'editor']


class IsBudgetOwner(permissions.BasePermission):
    """
    Permission to check if user is the owner of the budget
    """
    def has_object_permission(self, request, view, obj):
        member = obj.budget_members.filter(user=request.user).first()
        return member and member.role == 'owner'
