
import google.auth

from djangae.environment import is_production_environment

from .service_account import ServiceAccountCredentials


def default(scopes=None):
    if is_production_environment():
        return ServiceAccountCredentials(scopes=scopes)
    else:
        return google.auth.default(scopes=scopes)[0]
