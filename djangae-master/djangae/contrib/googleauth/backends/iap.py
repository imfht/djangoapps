import logging

from django.contrib.auth import get_user_model

from djangae.contrib.googleauth.models import UserManager

from . import _find_atomic_decorator, _generate_unused_username
from .base import BaseBackend

User = get_user_model()


class IAPBackend(BaseBackend):

    @classmethod
    def can_authenticate(cls, request):
        return "HTTP_X_GOOG_AUTHENTICATED_USER_ID" in request.META and \
            "HTTP_X_GOOG_AUTHENTICATED_USER_EMAIL" in request.META

    def authenticate(self, request, **kwargs):
        atomic = _find_atomic_decorator(User)

        user_id = request.META.get("HTTP_X_GOOG_AUTHENTICATED_USER_ID")
        email = request.META.get("HTTP_X_GOOG_AUTHENTICATED_USER_EMAIL")

        # User not logged in to IAP
        if not user_id or not email:
            return

        # All IDs provided should be namespaced
        if ":" not in user_id or ":" not in email:
            return

        # Google tokens are namespaced with "auth.google.com:"
        namespace, user_id = user_id.split(":", 1)
        _, email = email.split(":", 1)

        email = UserManager.normalize_email(email)
        assert email

        username = email.split("@", 1)[0]

        with atomic():
            # Look for a user, either by ID, or email
            user = User.objects.filter(google_iap_id=user_id).first()
            if not user:
                # We explicitly don't do an OR query here, because we only want
                # to search by email if the user doesn't exist by ID. ID takes
                # precendence.
                user = User.objects.filter(email_lower=email.lower()).first()

                if user and user.google_iap_id:
                    logging.warning(
                        "Found an existing user by email (%s) who had a different "
                        "IAP user ID (%s != %s). This seems like a bug.",
                        email, user.google_iap_id, user_id
                    )

                    # We don't use this to avoid accidentally "stealing" another
                    # user
                    user = None

            if user:
                # So we previously had a user sign in by email, but not
                # via IAP, so we should set that ID
                if not user.google_iap_id:
                    user.google_iap_id = user_id
                    user.google_iap_namespace = namespace
                else:
                    # Should be caught above if this isn't the case
                    assert(user.google_iap_id == user_id)

                # Update the email as it might have changed or perhaps
                # this user was added through some other means and the
                # sensitivity of the email differs etc.
                user.email = email

                # Note we don't update the username, as that may have
                # been overridden by something post-creation
                user.save()
            else:
                with atomic():
                    # First time we've seen this user
                    user = User.objects.create(
                        google_iap_id=user_id,
                        google_iap_namespace=namespace,
                        email=email,
                        username=_generate_unused_username(username)
                    )
                    user.set_unusable_password()
                    user.save()

        return user
