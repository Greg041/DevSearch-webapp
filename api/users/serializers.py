import email
from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {"email": {"required": True, "error_messages": {"required": "You need to provide an email"}}, 
                        "username": {"error_messages": {"required": "You need to provide a username"}}}


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"