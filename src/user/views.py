"""
File with the user views.
"""

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import User
from user.serializers import UserSerializer


class UserView(APIView):
    """
    View for list and create user.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Create a user.
        """
        if request.data.get('email'):
            user = User.objects.filter(email=request.data['email']).first()
            if user:
                return Response(
                    {"message": "Error creating user, email already exists"}, status=status.HTTP_400_BAD_REQUEST
                )
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """
        Update a user.
        """
        user_id = self.request.data.get('id', self.request.user.id)
        if not user_id:
            return Response({"message": "User id not found"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(id=user_id).first()
        if not user:
            return Response({"message": f"User with id {user_id} not found"}, status=status.HTTP_404_NOT_FOUND)
        if request.data.get('email'):
            user = User.objects.filter(email=request.data['email']).first()
            if user and user.id != user_id:
                return Response(
                    {"message": "Error updating user, email already exists"}, status=status.HTTP_400_BAD_REQUEST
                )
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User updated successfully"}, status=status.HTTP_200_OK)
        return Response(
            {"message": "Error updating user", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class UserListView(APIView):
    """
    View for list users
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Get all users.
        """
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailView(APIView):
    """
    View for return the user detail.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Get details of user logged in.
        """
        user_id = self.request.query_params.get('id', self.request.user.id)
        if not user_id:
            return Response({"message": "User id not found"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(id=user_id).first()
        if not user:
            return Response({"message": f"User with id {user_id} not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
