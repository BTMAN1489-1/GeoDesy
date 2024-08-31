from rest_framework import permissions

__all__ = (
    "StaffOnlyPermission",
)


class StaffOnlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if hasattr(user, "is_staff"):
            return user.is_staff
        return False
