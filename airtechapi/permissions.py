from rest_framework import permissions


class AnonymousPermissionOnly(permissions.BasePermission):
    """
    Check for Non-authenticated users only
    """
    message = 'You are already authenticated, please log out to continue.'

    def has_permission(self, request, view):
        return not request.user.is_authenticated


class IsAdminOrReadOnly(permissions.BasePermission):
    message = 'You must be the owner of this content to change it.'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff


class IsCurrentUserOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.passenger == request.user
