"""
File for the user serializer.
"""
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.urls import exceptions as url_exceptions
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, serializers
from rest_framework.exceptions import ValidationError

from user.models import User

# Get the User model
UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        """
        Class for metadata.
        """

        model = User
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class CustomUserDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for the user object.
    """

    class Meta:
        """
        Class for metadata.
        """

        model = get_user_model()
        fields = [
            'id',
            'email',
            'is_staff',
            'is_superuser',
            'first_name',
            'last_name',
            'phone_number',
            "profile_image",
        ]

    def to_representation(self, instance):
        """
        Method for representation of the user.
        """
        if not instance.is_active:
            raise ValidationError({'error': 'This user is not active'})
        representation = super().to_representation(instance)
        data = {'data': representation}
        return data


class CustomLoginSerializer(serializers.Serializer):
    """
    Serializer for the login object.
    """

    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def authenticate(self, **kwargs):
        """
        Method for authenticate the user.
        """
        return authenticate(self.context['request'], **kwargs)

    def _validate_email(self, email, password):
        """
        Method for validate the email.
        """
        if email and password:
            user = self.authenticate(email=email.lower(), password=password)
        else:
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def _validate_username(self, username, password):
        """
        Method for validate the username.
        """
        if username and password:
            user = self.authenticate(username=username.lower(), password=password)
        else:
            msg = _('Must include "username" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def _validate_username_email(self, email, password):
        """
        Method for validate the username and email.
        """
        if email and password:
            user = self.authenticate(email=email.lower(), password=password)
        else:
            msg = _('Must include either "email" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def get_auth_user_using_allauth(self, email, password):
        """
        Method for get the user using allauth.
        """
        if settings.AUTHENTICATION_METHOD == 'email':
            return self._validate_email(email, password)

        return self._validate_username_email(email, password)

    def get_auth_user(self, email, password):
        """
        Method for get the user.
        """
        if 'allauth' in settings.INSTALLED_APPS:
            try:
                return self.get_auth_user_using_allauth(email, password)
            except url_exceptions.NoReverseMatch as exc:
                msg = _('Unable to log in with provided credentials.')
                raise exceptions.ValidationError(msg) from exc
        return self._validate_username_email(email, password)

    @staticmethod
    def validate_auth_user_status(user):
        """
        Method for validate the user status, if is active or not.
        """
        if not user.is_active:
            msg = _('User account is disabled.')
            raise exceptions.ValidationError(msg)

    def validate(self, attrs):
        """
        Method for validate the user.
        """
        email = attrs.get('email')
        password = attrs.get('password')
        user = self.get_auth_user(email, password)
        if not user:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)
        self.validate_auth_user_status(user)

        attrs['user'] = user
        return attrs
