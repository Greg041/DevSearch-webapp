from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework import status
from django.db.models import Q
from functools import reduce
import operator
from projects.models import Review, Project
from api.projects.serializers import ProjectSerializer, CreateProjectSerializer
from projects.models import Tag


class ProjectsApiView(ListCreateAPIView):
    """ Return all projects posted on the webapp"""
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = CreateProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        owner = request.user.profile
        query = reduce(operator.or_, (Q(name__iexact=tag) for tag in request.data.get('tags')))  # Query used to search for tags recieved with case insensitive in the model Tag
        tags = Tag.objects.filter(query)
        self.perform_create(serializer, owner, tags)      
        headers = self.get_success_headers(serializer.data)
        return Response({"success": "Project created successfully"}, status=status.HTTP_201_CREATED, headers=headers)
        
    def perform_create(self, serializer, owner, tags):
        serializer.save(owner=owner, tags=tags)


class ProjectCrudApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def delete(self, request, *args, **kwargs):
        if request.user.profile == self.get_object().owner:
            return self.destroy(request, *args, **kwargs)
        else:
            return Response({'error': 'only the user of this project can delete it'}, status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, *args, **kwargs):
        if request.user.profile == self.get_object().owner:
            return self.update(request, *args, **kwargs)
        else:
            return Response({'error': 'only the user of this project can update it'}, status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request, *args, **kwargs):
        if request.user.profile == self.get_object().owner:
            return self.partial_update(request, *args, **kwargs)
        else:
            return Response({'error': 'only the user of this project can update it'}, status=status.HTTP_401_UNAUTHORIZED)
    


class VoteProjectApiView(CreateAPIView):
    permission_classes = [IsAuthenticated]

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
