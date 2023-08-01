"""
This module defines the model for the Django app 'authentication'.
"""

from datetime import timedelta

from django.db import models

from core.models import BaseModel
from user.models import User


class OTP(BaseModel):
    """
    Model for storing OTP (One-Time Password) codes.

    This class represents a Django model used for storing One-Time Password codes.
    It has fields for the user associated with the OTP, the code itself, the creation time,
    the update time, and the expiration time. The main functionality of this class is to
    save OTP instances and set their expiration time.

    Fields:
    - user: A foreign key to the user model of the Django authentication system.
            It represents the user associated with the OTP.
    - code: A character field with a maximum length of 6. It represents the OTP code itself.
    - created_at: A DateTimeField that is automatically set to the current time when the OTP instance is created.
    - update_at: A DateTimeField that is automatically updated to the current time whenever the OTP instance is saved.
    - is_active: A BooleanField that represents whether the OTP instance is active or not.
    - expires_at: A DateTimeField that represents the expiration time of the OTP instance.
                  It is set to 10 minutes after the creation time by the pre_save signal.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    validity_duration = models.PositiveIntegerField(default=10)

    def expires_at(self):
        return self.created_at + timedelta(minutes=self.validity_duration)

    def save(self, *args, **kwargs):
        """
        Save the OTP instance and set the expiration time.

        ... (resto de tu código)
        """
        super().save(*args, **kwargs)
