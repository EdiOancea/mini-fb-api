from app.permissions import BasePermission

class IsOwner(BasePermission):
    def has_permission(self, request, view):
        try:
            return request.data['user'] == request.user.id
        except (KeyError):
            return True
