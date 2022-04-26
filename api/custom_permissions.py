from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission
from users.models import Profile


class IsOwner(BasePermission):
    """Check is the authenticated user is the same as the user related to endpoint id"""
    def has_permission(self, request, view):
        profile_instance = get_object_or_404(Profile, id=view.kwargs.get('pk'))
        return request.user == profile_instance.user if request.user.is_authenticated and profile_instance else True
