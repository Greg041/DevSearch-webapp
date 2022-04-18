from django.contrib.auth.models import AbstractUser, PermissionsMixin, Group, Permission, User
from django.utils.translation import gettext_lazy as _
from django.db import models


class UserProfile(AbstractUser, PermissionsMixin):
    email = models.EmailField(_("email address"))  # Email needs to be mandatory so the system can sent an email once the user is registered
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['username', 'email']
    groups = models.ManyToManyField(
        Group,
        verbose_name=_("groups"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="user_set_api",
        related_query_name="user_api",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("user permissions"),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="user_set_api",
        related_query_name="user_api",
    )