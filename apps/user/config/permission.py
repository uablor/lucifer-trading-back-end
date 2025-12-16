from rest_framework import permissions
from shared.utils.permission import HasAnyPermission


class UserPermission(HasAnyPermission):
    def __init__(self):
        required_permissions = {
            'GET': ['account.view_user'],
            'POST': ['account.add_user'],
            'PUT': ['account.change_user'],
            'PATCH': ['account.change_user'],
            'DELETE': ['account.soft_delete_user'],   # 👈 soft delete
            'HARD_DELETE': ['account.hard_delete_user'], # 👈 custom
        }
        super().__init__(required_permissions)

    def has_permission(self, request, view):
        # handle custom hard delete (สมมุติคุณ map HTTP method หรือ action)
        if getattr(view, 'action', None) == 'hard_delete':
            return request.user.has_perm('account.hard_delete_user')
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj.is_superuser and request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return False
        return super().has_object_permission(request, view, obj)
