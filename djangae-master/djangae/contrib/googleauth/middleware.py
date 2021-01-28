
import hashlib
import logging
import os

from django import forms
from django.conf import settings
from django.contrib.auth import (
    BACKEND_SESSION_KEY,
    HASH_SESSION_KEY,
    REDIRECT_FIELD_NAME,
    _get_user_session_key,
    get_backends,
    constant_time_compare,
    load_backend,
    login,
    logout,
)
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls.base import reverse
from django.utils.functional import SimpleLazyObject
from django.utils.http import urlencode


from djangae.environment import is_production_environment

from .backends.iap import IAPBackend
from .backends.oauth2 import OAuthBackend
from .models import OAuthUserSession


_OAUTH_LINK_EXPIRY_SETTING = "GOOGLEAUTH_LINK_OAUTH_SESSION_EXPIRY"


def get_user_object(request):
    """
    Return the user model instance associated with the given request session.
    If no user is retrieved, return an instance of `AnonymousUser`.
    """
    from .models import AnonymousUser

    user = None
    try:
        user_id = _get_user_session_key(request)
        backend_path = request.session[BACKEND_SESSION_KEY]
    except KeyError:
        pass
    else:
        if backend_path in settings.AUTHENTICATION_BACKENDS:
            backend = load_backend(backend_path)
            user = backend.get_user(user_id)
            # Verify the session
            if hasattr(user, 'get_session_auth_hash'):
                session_hash = request.session.get(HASH_SESSION_KEY)
                session_hash_verified = session_hash and constant_time_compare(
                    session_hash,
                    user.get_session_auth_hash()
                )
                if not session_hash_verified:
                    request.session.flush()
                    user = None

    return user or AnonymousUser()


def get_user(request):
    if not hasattr(request, '_cached_user'):
        request._cached_user = get_user_object(request)
    return request._cached_user


class AuthenticationMiddleware(AuthenticationMiddleware):
    def process_request(self, request):
        assert hasattr(request, 'session'), (
            "The djangae.contrib.googleauth middleware requires session middleware "
            "to be installed. Edit your MIDDLEWARE%s setting to insert "
            "'django.contrib.sessions.middleware.SessionMiddleware' before "
            "'djangae.contrib.googleauth.middleware.AuthenticationMiddleware'."
        ) % ("_CLASSES" if settings.MIDDLEWARE is None else "")

        request.user = SimpleLazyObject(lambda: get_user(request))

        # See if the handling view is marked with the auth_middleware_exempt
        # decorator, and return if so.
        if request.resolver_match:
            func = request.resolver_match.func
            exempt = getattr(func, "_auth_middleware_exempt", False)
            if exempt:
                return None

        backend_str = request.session.get(BACKEND_SESSION_KEY)

        if request.user.is_authenticated:
            if backend_str and isinstance(load_backend(backend_str), OAuthBackend):

                # Should we link the Django session to the OAuth session? In most cases we shouldn't
                # as oauth would've been used for identification at login only.
                expire_session = getattr(settings, _OAUTH_LINK_EXPIRY_SETTING, False)

                if expire_session:
                    # The user is authenticated with Django, and they use the OAuth backend, so they
                    # should have a valid oauth session
                    oauth_session = OAuthUserSession.objects.filter(
                        pk=request.user.google_oauth_id
                    ).first()

                    # Their oauth session does not exist, so let's log them out
                    if not oauth_session:
                        logout(request)
                        return None

                    # Their oauth session expired but we still have an active user session
                    if not oauth_session.is_valid:
                        return redirect(
                            reverse("googleauth_oauth2login") + '?' + urlencode(dict(next=request.path))
                        )

            elif backend_str and isinstance(load_backend(backend_str), IAPBackend):
                if not IAPBackend.can_authenticate(request):
                    logout(request)
        else:
            backends = get_backends()
            try:
                iap_backend = next(filter(lambda be: isinstance(be, IAPBackend), backends))
            except StopIteration:
                iap_backend = None

            # Try to authenticate with IAP if the headers
            # are available
            if iap_backend and IAPBackend.can_authenticate(request):
                user = iap_backend.authenticate(request)
                if user and user.is_authenticated:
                    user.backend = 'djangae.contrib.googleauth.backends.iap.%s' % IAPBackend.__name__
                    login(request, user)


class ProfileForm(forms.Form):
    email = forms.EmailField()


_CREDENTIALS_FILE = os.path.join(
    settings.BASE_DIR, ".iap-credentials"
)


def _login_view(request):
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            # We write a credentials file for 2 reasons:
            # 1. It will persist across local server restarts.
            # 2. It will blow up on production, as the local folder
            #    is not writable.
            with open(_CREDENTIALS_FILE, "w") as f:
                f.write(
                    "%s\n" % (
                        form.cleaned_data["email"]
                    )
                )

            dest = request.GET.get(REDIRECT_FIELD_NAME, "/")
            return HttpResponseRedirect(dest)
    else:
        form = ProfileForm()

    subs = {
        "form": form
    }

    return render(request, "googleauth/dev_login.html", subs)


def id_from_email(email):
    """
        Just generates a predictable user ID from the email entered
    """
    md5 = hashlib.md5()
    md5.update(email.encode("utf-8"))

    # Truncate to 32-bit
    return int(md5.hexdigest(), 16) & 0xFFFFFFFF


def local_iap_login_middleware(get_response):
    def middleware(request):
        if is_production_environment():
            logging.warning(
                "local_iap_login_middleware is for local development only, "
                "and will not work on production. "
                "You should remove it from your MIDDLEWARE setting"
            )
            response = get_response(request)
        elif request.path == "/_dj/login/":
            response = _login_view(request)
        elif request.path == "/_dj/logout/":
            if os.path.exists(_CREDENTIALS_FILE):
                os.remove(_CREDENTIALS_FILE)

            if REDIRECT_FIELD_NAME in request.GET:
                return HttpResponseRedirect(request.GET[REDIRECT_FIELD_NAME])
            else:
                return HttpResponseRedirect("/_dj/login/")
        else:
            if os.path.exists(_CREDENTIALS_FILE):
                # Update the request headers with the stored credentials
                with open(_CREDENTIALS_FILE, "r") as f:
                    data = f.read()
                    email = data.strip()

                    request.META["HTTP_X_GOOG_AUTHENTICATED_USER_ID"] = "auth.example.com:%s" % id_from_email(email)
                    request.META["HTTP_X_GOOG_AUTHENTICATED_USER_EMAIL"] = "auth.example.com:%s" % email

            response = get_response(request)

        return response
    return middleware


LocalIAPLoginMiddleware = local_iap_login_middleware
