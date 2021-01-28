
from django.urls import path

from .views import oauth2callback, oauth_login


urlpatterns = (
    path('oauth2/callback/', oauth2callback, name="googleauth_oauth2callback"),
    path('oauth2/login/', oauth_login, name="googleauth_oauth2login"),
)
