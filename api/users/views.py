from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.users.serializers import UserProfileSerializer


class UserRegistrationApiView(APIView):
    """Handles user registration"""
    def post(self, request):
        user = UserProfileSerializer(data=request.data)
        if user.is_valid():
            user.save()
            return Response({'success': 'user was registered successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': user.error_messages}, status=status.HTTP_400_BAD_REQUEST)
