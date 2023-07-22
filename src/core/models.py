"""
File for models of the app core.
"""
from django.db import models


class BaseModel(models.Model):
    """
    Base model for all models.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        """
        Class for metadata.
        """

        abstract = True
