from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework import status
from django.db.models.query import QuerySet
from django.db.models import Q
from functools import reduce
import operator

from projects.models import Project
from api.projects.serializers import ProjectSerializer, CreateProjectSerializer, ReviewSerializer
from api.custom_pagination import CustomPageNumberPagination
from projects.models import Tag
from projects.utils import search_projects



class ProjectsApiView(ListCreateAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        if self.request.query_params.get('search'):
            query = self.request.query_params['search']
            tags = Tag.objects.filter(name__icontains=query)
            queryset = self.queryset.distinct().filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(owner__name__icontains=query) | Q(tags__in=tags)).exclude(featured_image='') 
        else:
            queryset = self.queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()
        return queryset

    def get(self, request, *args, **kwargs):
        """Return list of all projects in database paginated through page number validation in the sent in URL, paginate the results by 3"""
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


class ReviewProjectApiView(CreateAPIView):
    """ Create a review for a project whose id is sent in the URL and only if the user authenticated is not the owner
    of the project """
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def create(self, request, *args, **kwargs):
        project = Project.objects.get(id=kwargs['pk'])
        # Getting the profile instance through the relationship between the user class and the profile class
        user = request.user.profile
        review = project.review_set.all().filter(owner=user)
        if user == project.owner:
            return Response({'error': "This user can't vote its own project"}, status=status.HTTP_403_FORBIDDEN)
        elif review.exists():
            return Response({'error': "This user already review this project (if you want to update the review, use the respective URL)"}, status=status.HTTP_403_FORBIDDEN)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer, user, project)
            project.get_votes_total
            return Response({'success': "Review was successfully submitted", 'data': serializer.data}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer, user, project):
        serializer.save(owner=user, project=project)


class UpdateReviewProjectView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer
    lookup_field = 'id'

    def get_queryset(self):
        project = Project.objects.get(id=self.kwargs['pk'])
        queryset = project.review_set.all()
        return queryset

    def update(self, request, *args, **kwargs):
        project = Project.objects.all()
        try:
            project = project.get(id=self.kwargs['pk'])
        except project.model.DoesNotExist:
            return Response({'detail': 'Not found a project with the id provided'}, status=status.HTTP_404_NOT_FOUND)
        # Getting the profile instance through the relationship between the user class and the profile class
        user = request.user.profile
        review = project.review_set.all()
        try:
            review = review.get(id=self.kwargs['id'])
        except review.model.DoesNotExist:
            return Response({'detail': 'Not found a review with the id provided'}, status=status.HTTP_404_NOT_FOUND)
        if review.owner == user:
            partial = kwargs.pop('partial', False)
            serializer = self.get_serializer(review, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response({'success': "Review was successfully submitted", 'data': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': "This user is not authorized to edit this review"}, status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, *args, **kwargs):
        """Update the review with the data send only if the user authenticated is the owner of the review"""
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """Update the review with the data send only if the user authenticated is the owner of the review"""
        return super().patch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """get the data from the review with the id send in URL"""
        return super().get(request, *args, **kwargs)