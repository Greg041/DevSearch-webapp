from api.projects.serializers import ProjectSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from projects.models import Review


class ProjectsApiView(APIView):
    
    """ Return a project information in case the url used has a pk filter else returns all projects published"""
    def get(self, request, pk=None):
        if pk is None:
            projects = ProjectSerializer.Meta.model.objects.all()
            projects_serialized = ProjectSerializer(projects, many=True)
            return Response(projects_serialized.data)
        else:
            project = ProjectSerializer.Meta.model.objects.get(id=pk)
            project_serialized = ProjectSerializer(project)
            return Response(project_serialized.data)
    

@api_view(['POST', 'PUT'])
@permission_classes([IsAuthenticated])
def vote_and_review_project_api_view(request, pk):
    project = ProjectSerializer.Meta.model.objects.get(id=pk)
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
