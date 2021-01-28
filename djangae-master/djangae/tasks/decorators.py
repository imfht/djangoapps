
from functools import wraps

from django.http import HttpResponseForbidden

from .environment import is_in_task, is_in_cron


def task_only(view_function):
    """ View decorator for restricting access to tasks (and crons) of the application
        only.
    """

    @wraps(view_function)
    def replacement(request, *args, **kwargs):
        if not any((is_in_task(), is_in_cron())):
            return HttpResponseForbidden("Access denied.")

        return view_function(request, *args, **kwargs)

    return replacement


def task_or_superuser_only(view_function):
    @wraps(view_function)
    def replacement(request, *args, **kwargs):
        is_superuser = (
            getattr(request, "user", None) and
            request.user.is_authenticated and
            request.user.is_superuser
        )

        if not any((is_superuser, is_in_task(), is_in_cron())):
            return HttpResponseForbidden("Access denied.")

        return view_function(request, *args, **kwargs)

    return replacement


def csrf_exempt_if_task(view_function):
    class Replacement(object):
        def __call__(self, request, *args, **kwargs):
            return view_function(request, *args, **kwargs)

        @property
        def csrf_exempt(self):
            return any((is_in_task(), is_in_cron()))

    return Replacement()
