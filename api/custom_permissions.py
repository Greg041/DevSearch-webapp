from rest_framework.permissions import BasePermission
from users.models import Profile


class IsOwner(BasePermission):
    """Check is the authenticated user is the same as the user related to endpoint id"""
    def has_permission(self, request, view):
        profile_instance = Profile.objects.filter(id=view.kwargs.get('pk')).first()
        return request.user == profile_instance.user if request.user.is_authenticated else True