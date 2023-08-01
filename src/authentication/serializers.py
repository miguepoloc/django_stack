"""
File for the authentication serializer.
"""
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from authentication.models import OTP


class LoginSerializer(TokenObtainPairSerializer):
    """
    Serializer class for user login credentials and JWT generation.

    This class extends the TokenObtainPairSerializer from the rest_framework_simplejwt library.
    It adds custom claims and data to the JWT payload, including the user's email, ID, name, and email.
    """

    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def get_token(self, cls, user):
        """
        Get the JSON Web Token (JWT) for the user.

        Overrides the parent class method to add custom claims to the JWT payload, including the user's email.

        Args:
            user: The user object.

        Returns:
            The JSON Web Token (JWT) with custom claims.
        """
        token = super(LoginSerializer, cls).get_token(user)

        # Add custom claims
        token['email'] = user.email
        return token

    def validate(self, attrs):
        """
        Validate the user's login credentials.

        Overrides the parent class method to add custom data to the response, including the user's ID, name, and email.

        Args:
            attrs: The user's login credentials.

        Returns:
            The validated data with custom data added to the response.
        """
        data = super().validate(attrs)

        # Add custom data to response
        data['id'] = self.user.id
        data['name'] = self.user.first_name + ' ' + self.user.last_name
        data['email'] = self.user.email

        return data


class OTPLoginSerializer(serializers.Serializer):
    """
    Serializer class for the OTP (One-Time Password) code.

    This class is used to serialize the OTP code and validate it.
    """

    def validate(self, attrs):
        """
        Validate the OTP code.

        This method validates the OTP code by checking if it is active and has not expired.

        Args:
            attrs: The OTP code.

        Returns:
            The validated data.
        """
        otp_code = self.initial_data["otp"]

        # Check if OTP code is active
        otp = OTP.objects.filter(code=otp_code).first()
        if not otp or not otp.is_active:
            raise serializers.ValidationError('Invalid OTP code.')

        # Check if OTP code has expired
        if otp.expires_at < timezone.now():
            raise serializers.ValidationError('OTP code has expired.')

        self.instance.is_active = False
        self.instance.save()

        return attrs

    def deactivate(self):
        """
        Deactivate the OTP code.
        """
        self.instance.is_active = False
        self.instance.save()

    def get_token(self):
        """
        Get the JSON Web Token (JWT) for the user.

        Returns:
            The JSON Web Token (JWT) for the user.
        """
        return AccessToken.for_user(self.instance.user)

    def get_refresh_token(self):
        """
        Get the refresh token for the user.

        Returns:
            The refresh token for the user.
        """
        return RefreshToken.for_user(self.instance.user)

    def to_representation(self, instance):
        """
        Convert the OTP code to a JSON representation.

        Args:
            instance: The OTP code.

        Returns:
            The JSON representation of the OTP code.
        """
        return {
            "access_token": self.get_token(),
            "refresh_token": self.get_refresh_token(),
            "user": {
                "id": instance.user.id,
                "name": instance.user.first_name + ' ' + instance.user.last_name,
                "email": instance.user.email,
            },
        }
