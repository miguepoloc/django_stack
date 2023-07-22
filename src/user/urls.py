"""
File that contains the urls of the user app.
"""
from django.urls import path

from user.views import UserView

APP_NAME = 'user'

urlpatterns = [
    path('', UserView.as_view(), name='user-list'),
]
