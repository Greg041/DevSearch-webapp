import email
from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import Profile
from api.models import UserProfile


"""Used to serialize data for user registration using UserProfileModel where email and username are mandatory requirements"""
class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'