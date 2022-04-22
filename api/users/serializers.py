from rest_framework import serializers
from django.contrib.auth.models import User
from api.projects.serializers import ProjectSerializer
from users.models import Profile, Skill, Message


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {"email": {"required": True, "error_messages": {"required": "You need to provide an email"}}, 
                        "username": {"error_messages": {"required": "You need to provide a username"}}}

    
class SkillSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Skill
        fields = ['id', 'name', 'description']
        extra_kwargs = {"name": {"required": True, "error_messages": {"required": "You need to specify a name for the skill"}}}


class ProfileSerializer(serializers.ModelSerializer):
    skills = serializers.SerializerMethodField()
    projects = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = "__all__"

    def get_skills(self, instance):
        skills_serialized = SkillSerializer(instance=instance.skill_set.all(), many=True)
        return skills_serialized.data

    def get_projects(self, instance):
        projects_serialized = ProjectSerializer(instance=instance.project_set.all(), many=True)
        return projects_serialized.data


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'

        