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
    owner = ProfileSerializer()
    tags = TagSerializer(many=True)
    review = serializers.SerializerMethodField('get_reviews')
    
    class Meta:
        ordering = ['-vote_ratio']
        model = Project
        fields = '__all__'

    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        reviews_serialized = ReviewSerializer(reviews, many=True)
        return reviews_serialized.data


class CreateProjectSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField(required=False)
    featured_image = serializers.ImageField(required=False)
    demo_link = serializers.CharField(max_length=2000, required=False)
    source_link = serializers.CharField(max_length=2000, required=False)

    def create(self, validated_data):
        instance = Project.objects.create(**validated_data)
        return instance

