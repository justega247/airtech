from rest_framework import permissions


class AnonymousPermissionOnly(permissions.BasePermission):
    """
    Check for Non-authenticated users only
    """
    message = 'You are already authenticated, please log out to continue.'

    def has_permission(self, request, view):
        return not request.user.is_authenticated
