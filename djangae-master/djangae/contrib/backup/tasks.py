import logging
import os

from django.apps import apps

import googleapiclient.discovery
from djangae.environment import (
    application_id,
    is_production_environment,
)
import google.auth
from google.oauth2 import service_account

from .utils import (
    get_backup_path,
    get_backup_setting,
)

logger = logging.getLogger(__name__)


AUTH_SCOPES = ['https://www.googleapis.com/auth/datastore']
SERVICE_URL = 'https://datastore.googleapis.com/$discovery/rest?version=v1'


def backup_datastore(bucket=None, kinds=None):
    """
    Using the new scheduled backup service write all required entity kinds
    to a specific GCS bucket path.
    """
    backup_enabled = get_backup_setting("ENABLED", False)
    if not backup_enabled:
        logger.warning(
            "DJANGAE_BACKUP_ENABLED is False or not set."
            "The datastore backup will not be run."
        )
        return

    # make sure no blacklisted entity kinds are included in our export
    valid_kinds = _get_valid_export_kinds(kinds)
    if not valid_kinds:
        logger.warning("No whitelisted entity kinds to export.")
        return

    # build the service object with the necessary credentials and trigger export
    service = _get_service()
    body = {
        'outputUrlPrefix': get_backup_path(bucket),
        'entityFilter': {
            'kinds': valid_kinds,
        }
    }
    app_id = application_id()
    request = service.projects().export(projectId=app_id, body=body)
    request.execute()


def _get_valid_export_kinds(kinds=None):
    """Make sure no blacklist models are included in our backup export."""
    excluded_models = get_backup_setting("EXCLUDE_MODELS", required=False, default=[])
    excluded_apps = get_backup_setting("EXCLUDE_APPS", required=False, default=[])

    to_backup = []
    for model in apps.get_models(include_auto_created=True):
        app_label = model._meta.app_label
        object_name = model._meta.object_name
        model_def = "{}_{}".format(app_label, object_name.lower())
        db_table = model._meta.db_table

        if app_label in excluded_apps:
            logger.info(
                "Not backing up %s due to the %s app being in DJANGAE_BACKUP_EXCLUDE_APPS",
                model_def, app_label
            )
            continue

        # Exclude the models if either the model label or datastore kind
        # is listed.
        if model_def in excluded_models or db_table in excluded_models:
            logger.info(
                "Not backing up %s as it is blacklisted in DJANGAE_BACKUP_EXCLUDE_MODELS",
                model_def
            )
            continue

        logger.info("%s added to list of models to backup", model_def)
        to_backup.append((model_def, db_table))

    # If kinds we explcitly provided by the caller, we only return those
    # already validated by our previous checks
    if kinds:
        to_backup = [
            kind for (_model_def, kind) in to_backup
            if _model_def in kinds or kind in kinds
        ]
    else:
        to_backup = [kind for (_model_def, kind) in to_backup]

    # If 2 models share the same underlying table they will return the same
    # kind. The datastore backup API will return a validation error when a kind
    # is listed more than once.
    return list(set(to_backup))


def _get_service():
    """Creates an Admin API service object for talking to the API."""
    credentials = _get_authentication_credentials()
    return googleapiclient.discovery.build(
        'admin', 'v1',
        credentials=credentials,
        discoveryServiceUrl=SERVICE_URL
    )


def _get_authentication_credentials():
    """
    Returns authentication credentials depending on environment. See
    https://developers.google.com/api-client-library/python/auth/service-accounts
    """
    if is_production_environment():
        credentials, _ = google.auth.default(scopes=AUTH_SCOPES)
    else:
        service_account_path = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
        credentials = service_account.Credentials.from_service_account_file(
            service_account_path, scopes=AUTH_SCOPES
        )
    return credentials
