import email
from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import Profile, Skill


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {"email": {"required": True, "error_messages": {"required": "You need to provide an email"}}, 
                        "username": {"error_messages": {"required": "You need to provide a username"}}}

    
class SkillSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Skill
        fields = '__all__'
        extra_kwargs = {"name": {"required": True, "error_messages": {"required": "You need to specify a name for the skill"}}}


class ProfileSerializer(serializers.ModelSerializer):
    skills = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = "__all__"

    def get_skills(self, instance):
        skills_serialized = SkillSerializer(instance.skill_set.all())
        return skills_serialized.data