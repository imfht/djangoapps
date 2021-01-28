default_app_config = 'djangae.contrib.googleauth.apps.GoogleauthConfig'

_CLIENT_ID_SETTING = "GOOGLEAUTH_CLIENT_ID"
_CLIENT_SECRET_SETTING = "GOOGLEAUTH_CLIENT_SECRET"
_DEFAULT_SCOPES_SETTING = "GOOGLEAUTH_OAUTH_SCOPES"
_DEFAULT_SCOPES_SETTING = "GOOGLEAUTH_OAUTH_SCOPES"
_OAUTH_REDIRECT_HOST = "GOOGLEAUTH_OAUTH_REDIRECT_HOST"

_SCOPE_SESSION_KEY = "_googleauth_scopes_requested"


def _stash_scopes(request, scopes, offline):
    """
        Stores requested scopes in the session
    """

    request.session[_SCOPE_SESSION_KEY] = (scopes, offline)


def _pop_scopes(request):
    return request.session.pop(_SCOPE_SESSION_KEY, ([], False))
