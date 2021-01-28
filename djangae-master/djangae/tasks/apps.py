import logging

from django.apps import AppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from google.api_core import exceptions


class DjangaeTasksConfig(AppConfig):
    name = "djangae.tasks"
    verbose_name = "Djangae Tasks"

    def ready(self):
        """
            On startup we ensure the required queues
            exist based on settings.CLOUD_TASKS_QUEUES
        """
        from . import ensure_required_queues_exist
        try:
            ensure_required_queues_exist()
        except exceptions.ServiceUnavailable:
            logging.warning("Not creating required queues as Cloud Tasks client is unavailable")

        if not getattr(settings, "CLOUD_TASKS_LOCATION", None):
            raise ImproperlyConfigured(
                "You must specify settings.CLOUD_TASKS_LOCATION "
                "to use the djangae.tasks app."
            )
