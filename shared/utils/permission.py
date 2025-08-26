from rest_framework import permissions

class IsVerified(permissions.BasePermission):
    """
    Custom permission to only allow verified users to access the view.
    """
    message = 'Please verify your email address...!'

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_verify

class HasAnyPermission(permissions.BasePermission):
    def __init__(self, required_permissions=None):
        self.required_permissions = required_permissions or {}
        
    def group_has_permission(self, request, view):
        pass

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        permissions_required = self.required_permissions.get(request.method, [])
        return any(request.user.has_perm(permission) for permission in permissions_required)
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)