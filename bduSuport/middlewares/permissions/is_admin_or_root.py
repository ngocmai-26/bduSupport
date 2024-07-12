from rest_framework import permissions

from bduSuport.models.account import AccountRole

class IsAdminOrRoot(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == AccountRole.ROOT or request.user.role == AccountRole.ADMIN