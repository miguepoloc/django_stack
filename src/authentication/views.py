"""
File with the authentication views.
"""
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from authentication.serializers import LoginSerializer
from user.models import User


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def handle_exception(self, exc):
        if isinstance(exc, AuthenticationFailed):
            return Response(
                {"message": "Error login, password incorrect", "status": status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().handle_exception(exc)

    def post(self, request):
        """
        Post method for login.
        """
        request_email = request.data.get('email')
        request_password = request.data.get('password')
        if not request_email or not request_password:
            return Response(
                {"message": "Error Email or Password not found", "status": status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if request.data.get('email'):
            user = User.objects.filter(email=request.data['email']).first()
            if not user:
                return Response(
                    {"message": "Error Email not found", "status": status.HTTP_400_BAD_REQUEST},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        response = super().post(request)

        refresh_token = response.data["refresh"]
        access_token = response.data["access"]
        user_id = response.data["id"]
        email = response.data["email"]
        name = response.data["name"]

        return Response(
            {
                "message": "User logged in successfully",
                "user_detail": {
                    "user_id": user_id,
                    "email": email,
                    "name": name,
                },
                "token": {
                    "refresh_token": refresh_token,
                    "access_token": access_token,
                },
                "status": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh_token")

        if not refresh_token:
            return Response(
                {"message": "Error refresh token not found", "status": status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            refresh = RefreshToken(refresh_token)
            refresh.blacklist()

            return Response(
                {"message": "Successfully logged out.", "status": status.HTTP_205_RESET_CONTENT},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except TokenError:
            return Response(
                {"message": "Invalid token.", "status": status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"message": "Error logout", "error": str(e), "status": status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LogoutAllView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            tokens = OutstandingToken.objects.filter(user_id=request.user.id)
            if not tokens:
                return Response(
                    {"message": "No active tokens for this user.", "status": status.HTTP_400_BAD_REQUEST},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            for token in tokens:
                BlacklistedToken.objects.get_or_create(token=token)

            return Response(
                {"message": "Successfully logged out all sessions.", "status": status.HTTP_205_RESET_CONTENT},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except TokenError:
            return Response(
                {"message": "Invalid token.", "status": status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"message": "Error logout", "error": e, "status": status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST,
            )
