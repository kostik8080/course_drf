from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Проверяет, что пользователь является владельцем."""

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        return False
