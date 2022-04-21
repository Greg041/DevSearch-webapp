from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.db.models.query import QuerySet
from api.users.serializers import UserSerializer, ProfileSerializer, SkillSerializer
from api.custom_permissions import IsOwner



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
    serializer_class = SkillSerializer
    permission_class = [IsAuthenticated&IsOwner]
    
    def get_queryset(self):
        queryset = self.request.user.profile.skill_set.all()
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = self.request.user.profile.skill_set.all()
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        owner = request.user.profile
        self.perform_create(serializer, owner)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, owner):
        serializer.save(owner=owner)