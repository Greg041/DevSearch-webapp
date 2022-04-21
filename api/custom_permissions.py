from rest_framework.permissions import BasePermission, IsAuthenticated


class IsOwner(BasePermission):
    """Check is the authenticated user is the same as the user related to the model"""
    def has_permission(self, request, view):
        return request.user == view.get_object().user if request.user.is_authenticated else True