import threading
from typing import Optional

from django.core.exceptions import ImproperlyConfigured

_TASK_ENV = threading.local()


def _check_task_environment_middleware():
    from django.conf import settings  # nested to prevent early-import

    check1 = "djangae.tasks.middleware.task_environment_middleware"
    check2 = "djangae.tasks.middleware.TaskEnvironmentMiddleware"

    enabled = any([x in settings.MIDDLEWARE for x in (check1, check2)])

    if not enabled:
        raise ImproperlyConfigured(
            "You must add djangae.tasks.middleware.TaskEnvironmentMiddleware "
            "to your MIDDLEWARE setting to make use of djangae.tasks.environment"
        )


def is_in_task() -> bool:
    "Returns True if the request is a task, False otherwise"
    _check_task_environment_middleware()
    return bool(getattr(_TASK_ENV, "task_name", False))


def is_in_cron() -> bool:
    "Returns True if the request is in a cron, False otherwise"
    _check_task_environment_middleware()
    return bool(getattr(_TASK_ENV, "is_cron", False))


def task_name() -> Optional[str]:
    "Returns the name of the current task if any, else None"
    _check_task_environment_middleware()
    return getattr(_TASK_ENV, "task_name", None)


def task_retry_count() -> Optional[int]:
    "Returns the task retry count, or None if this isn't a task"
    _check_task_environment_middleware()
    try:
        return int(getattr(_TASK_ENV, "task_retry_count", None))
    except (TypeError, ValueError):
        return None


def task_queue_name() -> Optional[str]:
    "Returns the name of the current task queue (if this is a task) else 'default'"
    _check_task_environment_middleware()
    if is_in_task():
        return getattr(_TASK_ENV, "queue_name", "default")
    return None


def task_execution_count() -> Optional[int]:
    _check_task_environment_middleware()
    if is_in_task():
        return getattr(_TASK_ENV, "task_execution_count", 0)
    return None
