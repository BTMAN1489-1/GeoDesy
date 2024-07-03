from rest_framework import permissions


class StaffOnlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if user is not None:
            return user.is_staff
        return False
