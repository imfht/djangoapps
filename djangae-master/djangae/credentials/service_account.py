# Work around the fact that google.auth.default doesn't support custom
# scopes on production

# Special thanks to David Buxton for this code
# https://gist.github.com/davidwtbuxton/525924b7f06f56b8530947d55bad1c21

import datetime

from google.auth import _helpers
from google.auth import credentials
from google.auth.compute_engine import _metadata


class ServiceAccountCredentials(credentials.Scoped, credentials.Credentials):
    """Credentials for App Engine runtime using the metadata service.
    In production `google.auth.default()` returns an instance of the Compute
    Engine credentials class, which does not currently support custom oauth
    scopes, even though it uses the metadata service which does.
    """

    def __init__(self, scopes=None, service_account_id="default"):
        super().__init__()
        self._scopes = scopes
        self._service_account_id = service_account_id

    def refresh(self, request):
        data = self._get_token(request, self._scopes)
        seconds = data["expires_in"]
        token_expiry = _helpers.utcnow() + datetime.timedelta(seconds=seconds)

        self.token = data["access_token"]
        self.expiry = token_expiry

    @classmethod
    def _get_token(cls, request, scopes=None):
        token_url = "instance/service-accounts/default/token"

        if scopes:
            if not isinstance(scopes, str):
                scopes = ",".join(scopes)

            token_url = _helpers.update_query(token_url, {"scopes": scopes})

        token_data = _metadata.get(request, token_url)

        return token_data

    @property
    def requires_scopes(self):
        return not self._scopes

    def with_scopes(self, scopes):
        return self.__class__(
            scopes=scopes, service_account_id=self._service_account_id
        )
