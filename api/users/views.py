from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q
from django.db.models.query import QuerySet
from django.db.models.aggregates import Count

from api.users.serializers import UserSerializer, ProfileSerializer, SkillSerializer, MessageSerializer
from api.custom_permissions import IsOwner
from users.models import Profile
from api.custom_pagination import CustomPageNumberPagination


class UserRegistrationApiView(CreateAPIView):
    """Register a new user in the database and automatically creates a profile for him with the basic data 
    sent to registration"""
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        user_data = super().post(request, *args, **kwargs)
        print(user_data.status_code)
        if user_data.status_code == 201:
            user_data.data = {"success": "The user was successfully created"}
            return user_data
        else:
            user_data.data = {"error": "There was a problem creating the user"}
            return user_data


class LogoutApiView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        token = request.auth
        RefreshToken.for_user(request.user)
        token.blacklist()
        return Response(status=status.HTTP_205_RESET_CONTENT)



class ListProfilesApiView(ListAPIView):
    """Return the list of all profiles registered in the webpage, paginate the results by 3"""
    serializer_class = ProfileSerializer
    queryset = ProfileSerializer.Meta.model.objects.all()
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        if self.request.query_params.get('search'):
            query = self.request.query_params['search']
            queryset = Profile.objects.filter(Q(name__icontains=query) | Q(short_intro__icontains=query)).distinct().exclude(profile_image='').annotate(projects_number=Count('project')).order_by('-projects_number')
            if not queryset:
                queryset = Profile.objects.get_profiles_by_skills(query).exclude(profile_image='').annotate(projects_number=Count('project')).order_by('-projects_number')
        else:
            queryset = self.queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()
        return queryset

    

class ProfileApiView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = ProfileSerializer.Meta.model.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly&IsOwner]

    def get(self, request, *args, **kwargs):
        """Return the all the public data for the profile whose id is sent through the endpoint"""
        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Update the data for the profile whose id sent only if the user is authenticated
        and is the owner of the profile"""
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """Update the data for the profile whose id sent only if the user is authenticated
        and is the owner of the profile"""
        return super().patch(request, *args, **kwargs)


class ProfileSkillsApiView(ListCreateAPIView):
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated&IsOwner]

    def get(self, request, *args, **kwargs):
        """Get the skills for the user id send through pk field and only if the user authenticated who send the request
            is the same as the user whose id is send, if the user doesn't have skills then a empty list is sent as a Response."""
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Create a skill for the user id send through pk field only if the user authenticated who send the request
        is the same as the user whose id is send
    
        return status code 201 when success"""
        return super().post(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = self.request.user.profile.skill_set.all()
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = self.request.user.profile.skill_set.all()
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['name'] = serializer.validated_data['name'].upper()
        owner = request.user.profile
        self.perform_create(serializer, owner)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, owner):
        serializer.save(owner=owner)


class ProfileSkillRUDApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated&IsOwner]
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        """Retrieve the data from a specific skill whose is sent through the URL only if the 
        user is authenticated and is owner of the skill"""
        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Update the data for a specific skill whose is sent through the URL only if the 
        user is authenticated and is owner of the skill"""
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """Update the data for a specific skill whose is sent through the URL only if the 
        user is authenticated and is owner of the skill"""
        return super().patch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.request.user.profile.skill_set.all()
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = self.request.user.profile.skill_set.all()
        return queryset

    def destroy(self, request, *args, **kwargs):
        """Deletes the data for a specific skill whose is sent through the URL only if the 
        user is authenticated and is owner of the skill"""
        response = super().destroy(request, *args, **kwargs)
        response.data = {'success': "The skill was deleted successfully"}
        return response


class MessagesApiView(ListAPIView):
    """Return all messages received for the user authenticated"""
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.request.user.profile.recipient_messages.all()
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = self.request.user.profile.recipient_messages.all()
        return queryset


class SingleMessageApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated&IsOwner]
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        """Return data for the message whose id is sent in the URL only if the user authenticated
        is the owner of the received message"""
        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Updates data for the message whose id is sent in the URL only if the user authenticated
        is the owner of the received message"""
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """Updates data for the message whose id is sent in the URL only if the user authenticated
        is the owner of the received message"""
        return super().patch(request, *args, **kwargs)


class SendMessageApiView(CreateAPIView):
    """Sents a message from the authenticated user to the user whose id is provided in the URL"""
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sender = request.user.profile
        try:
            recipient = Profile.objects.get(id=kwargs['pk'])
            if recipient == sender:
                return Response({"error": "You can't send a message to yourself"}, status=status.HTTP_409_CONFLICT)
        except:
            return Response({"error": "The user you want to send a message doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        self.perform_create(serializer, sender, recipient)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, sender, recipient):
        serializer.save(sender=sender, recipient=recipient, sender_name=sender.name, sender_email=sender.email)
