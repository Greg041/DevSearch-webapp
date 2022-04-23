from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.conf import settings


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_message = f"{reverse('password_reset:reset-password-request')}?token={reset_password_token.key}"
    send_mail(
        subject = "Password Reset for Devsearch",
        message = email_message,
        from_email = settings.EMAIL_HOST_USER,
        recipient_list = [reset_password_token.user.email]
    )