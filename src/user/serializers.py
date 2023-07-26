"""
File for the user serializer.
"""
from django.contrib.auth import get_user_model
from rest_framework import serializers
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
        if validated_data.get('email'):
            validated_data['email'] = validated_data['email'].lower()
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

    def to_representation(self, instance):
        """
        Method for representation of the user.
        """
        if not instance.is_active:
            raise ValidationError({'error': 'This user is not active'})
        data = {
            'id': instance.id,
            'email': instance.email,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'document': instance.document,
            'phone_number': instance.phone_number,
            'is_active': instance.is_active,
            'created_at': instance.created_at,
        }
        return data


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
