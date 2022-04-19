from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework import status
from projects.models import Review, Project
from api.projects.serializers import ProjectSerializer


class ReturnProjectsApiView(APIView):
    """ Return all projects posted on the webapp, in case a project id is sent as a parameter through the endpoint
    returns the info of the project with such id"""
    def get(self, request, pk=None):
        if pk is None:
            projects = ProjectSerializer.Meta.model.objects.all()
            projects_serialized = ProjectSerializer(projects, many=True)
            return Response(projects_serialized.data)
        else:
            project = ProjectSerializer.Meta.model.objects.get(id=pk)
            project_serialized = ProjectSerializer(project)
            return Response(project_serialized.data)


class VoteProjectApiView(CreateAPIView):

    @permission_classes([IsAuthenticated])
    def post(self, request, pk):
        project = Project.objects.get(id=pk)
        # Getting the profile instance through the relationship between the user class and the profile class
        user = request.user.profile
        review, created = Review.objects.get_or_create(owner=user, project=project)
        if user == project.owner:
            return Response({'error': "You can't vote your own project"})
        elif request.data.get('value'):
            review.value = request.data['value']
            review.body = request.data['body'] if request.data.get('body') else ''
            review.save()
            project.get_votes_total
            project_serialized = ProjectSerializer(project)
            return Response(project_serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'You must provide a vote value for the review and a review comment(optional)'}, status=status.HTTP_400_BAD_REQUEST)
