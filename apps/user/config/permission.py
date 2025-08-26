from rest_framework import permissions
from shared.utils.permission import HasAnyPermission


class UserPermission(HasAnyPermission):
    def __init__(self):
        required_permissions = {
            'GET': ['account.view_user'],
            'POST': ['account.add_user'],
            'PUT': ['account.change_user'],
            'PATCH': ['account.change_user'],
            'DELETE': ['account.delete_user']
        }
        super().__init__(required_permissions)

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj.is_superuser and request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return False
        return super().has_object_permission(request, view, obj)

class GroupPermission(HasAnyPermission):
    def __init__(self):
        required_permissions = {
            'GET': ['auth.view_group'],
            'POST': ['auth.add_group'],
            'PUT': ['auth.change_group'],
            'PATCH': ['auth.change_group'],
            'DELETE': ['auth.delete_group']
        }
        super().__init__(required_permissions)

class PermissionPermission(HasAnyPermission):
    def __init__(self):
        required_permissions = {
            'GET': ['auth.view_permission'],
            'POST': ['auth.add_permission'],
            'PUT': ['auth.change_permission'],
            'PATCH': ['auth.change_permission'],
            'DELETE': ['auth.delete_permission']
        }

        super().__init__(required_permissions)
