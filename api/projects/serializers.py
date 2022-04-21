from rest_framework import serializers
from projects.models import Project, Tag, Review
from api.users.serializers import ProfileSerializer

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['-vote_ratio']
        model = Project
        fields = '__all__'


    def to_representation(self, instance):
        return {
            "id": instance.id,
            "owner": ProfileSerializer(instance.owner).data,  # Return all values serialized from related field
            "title": instance.title,
            "description": instance.description,
            "featured_image": instance.featured_image.url,
            "demo_link": instance.demo_link,
            "source_link": instance.source_link,
            "tags": TagSerializer(instance.tags, many=True).data,  # Return all values serialized from related field
            "vote_total": instance.vote_total,
            "vote_ratio": instance.vote_ratio,
            "created": instance.created,
            "review": ReviewSerializer(instance.review_set.all(), many=True).data # I also want to retrieve the reviews related data
        }


class CreateProjectSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField(required=False)
    featured_image = serializers.ImageField(required=False)
    demo_link = serializers.CharField(max_length=2000, required=False)
    source_link = serializers.CharField(max_length=2000, required=False)

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        instance = Project.objects.create(**validated_data)
        instance.tags.add(*tags)
        return instance

