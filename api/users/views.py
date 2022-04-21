from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView
from api.users.serializers import UserSerializer, ProfileSerializer



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
    permission_classes = []