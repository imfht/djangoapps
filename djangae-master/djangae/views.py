import logging
from importlib import import_module

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from djangae import environment
from djangae.tasks import decorators
from djangae.core.signals import module_started, module_stopped


logger = logging.getLogger(__name__)


def warmup(request):
    """
        Provides default procedure for handling warmup requests on App
        Engine. Just add this view to your main urls.py.
    """
    for app in settings.INSTALLED_APPS:
        for name in ('urls', 'views', 'models'):
            try:
                import_module('%s.%s' % (app, name))
            except ImportError:
                pass
    return HttpResponse("OK")


def start(request):
    module_started.send(sender=__name__, request=request)
    return HttpResponse("OK")


def stop(request):
    module_stopped.send(sender=__name__, request=request)
    return HttpResponse("OK")


@csrf_exempt
def deferred(request):
    from google.appengine.ext.deferred.deferred import (
        run,
        SingularTaskFailure,
        PermanentTaskFailure
    )

    response = HttpResponse()

    if 'HTTP_X_APPENGINE_TASKEXECUTIONCOUNT' in request.META:
        logger.debug("[DEFERRED] Retry %s of deferred task", request.META['HTTP_X_APPENGINE_TASKEXECUTIONCOUNT'])

    if 'HTTP_X_APPENGINE_TASKNAME' not in request.META:
        logger.critical('Detected an attempted XSRF attack. The header "X-AppEngine-Taskname" was not set.')
        response.status_code = 403
        return response

    in_prod = environment.is_production_environment()

    if in_prod and request.META.get("REMOTE_ADDR") != "0.1.0.2":
        logger.critical('Detected an attempted XSRF attack. This request did not originate from Task Queue.')
        response.status_code = 403
        return response

    try:
        run(request.body)
    except SingularTaskFailure:
        logger.debug("Failure executing task, task retry forced")
        response.status_code = 408
    except PermanentTaskFailure:
        logger.exception("Permanent failure attempting to execute task")

    return response


@decorators.task_only
def clearsessions(request):
    engine = import_module(settings.SESSION_ENGINE)
    try:
        engine.SessionStore.clear_expired()
    except NotImplementedError:
        logger.exception(
            "Session engine '%s' doesn't support clearing "
            "expired sessions.\n", settings.SESSION_ENGINE
        )
    return HttpResponse("OK")
