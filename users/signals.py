from django.core.mail import send_mail
from django.conf import settings
from .models import Profile


def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
            username = user.username,
            email = user.email,
            name = user.first_name
        )

        send_mail(
            'Welcome', 
            """Welcome to devsearch project, we hope this platform helps you making your work
            recognized by other people""",
            settings.EMAIL_HOST_USER,
            [user.email], 
            fail_silently=False)


"""The sender will be a profile instance with which will be updated the user instance
linked to it"""
def update_profile(sender, instance, created, **kwargs):
    if not created:
        user = instance.user
        user.first_name = instance.name
        user.username = instance.username
        user.email = instance.email
        user.save()



def delete_user(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass
