from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.db.models.query import QuerySet
from api.users.serializers import UserSerializer, ProfileSerializer, SkillSerializer, MessageSerializer
from api.custom_permissions import IsOwner
from users.models import Profile


class UserRegistrationApiView(CreateAPIView):
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


class ListProfilesApiView(ListAPIView):
    serializer_class = ProfileSerializer
    queryset = ProfileSerializer.Meta.model.objects.all()


class ProfileApiView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = ProfileSerializer.Meta.model.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly&IsOwner]


class ProfileSkillsApiView(ListCreateAPIView):
    """Get the skills for the user id send through pk field and only if the user authenticated who send the request
    is the same as the user whose id is send, if the user doesn't have skills then a empty list is sent as a Response.
    
    Create a skill for the user id send through pk field only if the user authenticated who send the request
    is the same as the user whose id is send
    
    return status code 201 when success"""

    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated&IsOwner]
    
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

    def get_queryset(self):
        queryset = self.request.user.profile.skill_set.all()
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = self.request.user.profile.skill_set.all()
        return queryset

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        response.data = {'success': "The skill was deleted successfully"}
        return response


class MessagesApiView(ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated&IsOwner]

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


class SendMessageApiView(CreateAPIView):
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
