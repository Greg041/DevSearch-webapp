from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        from users import signals
        from django.contrib.auth.models import User
        post_save.connect(signals.create_profile, sender=User)
        post_save.connect(signals.update_profile, sender='users.Profile')
        post_delete.connect(signals.delete_user, sender='users.Profile')

