from rest_framework.permissions import SAFE_METHODS

from app.permissions import BasePermission

class IsOwner(BasePermission):
    def has_permission(self, request, view):
        try:
            return request.data['user'] == request.user.id
        except (KeyError):
            return True

class IsOwnerOrReadOnly(IsOwner):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or super(IsOwner, self).has_permission
