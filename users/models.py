# Django imports
from django.db import models
from django.conf import settings
from django.templatetags.static import static
# Third party imports
import uuid
from cloudinary.models import CloudinaryField


# Create your models here.
class ProfileQuerySet(models.QuerySet):
    def get_profiles_by_skills(self, query):
        skills = Skill.objects.filter(name__icontains=query)
        return self.filter(skill__in=skills).distinct()


class Profile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    short_intro = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = CloudinaryField("Profile image", null=True, blank=True)
    social_github = models.CharField(max_length=200, blank=True, null=True)
    social_twitter = models.CharField(max_length=200, blank=True, null=True)
    social_linkedin = models.CharField(max_length=200, blank=True, null=True)
    social_youtube = models.CharField(max_length=200, blank=True, null=True)
    personal_website = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = ProfileQuerySet.as_manager()

    def __str__(self):
        return str(self.user.username)

    @property
    def get_image_url(self):
        if self.profile_image:
            return self.profile_image.url
        return static("images/no-user-image.png")


class Skill(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="recipient_messages")
    sender_name = models.CharField(max_length=200, null=True, blank=True)
    sender_email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['is_read', 'created']

    def save(self, *args, **kwargs):
        self.sender_name = self.sender.name
        self.sender_email = self.sender.email 
        return super().save(*args, **kwargs)

