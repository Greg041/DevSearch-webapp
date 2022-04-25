from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework import status
from django.db.models import Q
from functools import reduce
import operator
from projects.models import Project
from api.projects.serializers import ProjectSerializer, CreateProjectSerializer, ReviewSerializer
from projects.models import Tag


class ProjectsApiView(ListCreateAPIView):
    """ Return list of projects posted on the webapp and create a new project when request method == POST """
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        """Return list of all projects in database paginated through page number validation in the sent in URL"""
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """ Post a new project if the user is authenticated with the data received """
        return super().post(request, *args, **kwargs)

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
        """Delete a the project whose id is sent through the endpoint only if the authenticated user is the owner of the project"""
        if request.user.profile == self.get_object().owner:
            return self.destroy(request, *args, **kwargs)
        else:
            return Response({'error': 'only the owner of this project can delete it'}, status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, *args, **kwargs):
        """Update a the project whose id is sent through the endpoint only if the authenticated user is the owner of the project"""
        if request.user.profile == self.get_object().owner:
            return self.update(request, *args, **kwargs)
        else:
            return Response({'error': 'only the owner of this project can update it'}, status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request, *args, **kwargs):
        """Update a the project whose id is sent through the endpoint only if the authenticated user is the owner of the project"""
        if request.user.profile == self.get_object().owner:
            return self.partial_update(request, *args, **kwargs)
        else:
            return Response({'error': 'only the owner of this project can update it'}, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request, *args, **kwargs):
        """Retrieve the project data whose id is sent through the endpoint"""
        return super().get(request, *args, **kwargs)


class VoteProjectApiView(CreateAPIView):
    """ Create a review for a project whose id is sent in the URL and only if the user authenticated is not the owner
    of the project """
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def create(self, request, *args, **kwargs):
        project = Project.objects.get(id=kwargs['pk'])
        # Getting the profile instance through the relationship between the user class and the profile class
        user = request.user.profile
        if user == project.owner:
            return Response({'error': "You can't vote your own project"}, status=status.HTTP_403_FORBIDDEN)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer, user, project)
            project.get_votes_total
            return Response({'success': "Review was successfully submitted"}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer, user, project):
        serializer.save(owner=user, project=project)

