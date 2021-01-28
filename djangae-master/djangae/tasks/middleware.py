from .environment import _TASK_ENV

_TASK_NAME_HEADER = "HTTP_X_APPENGINE_TASKNAME"
_QUEUE_NAME_HEADER = "HTTP_X_APPENGINE_QUEUENAME"
_TASK_EXECUTION_COUNT_HEADER = "HTTP_X_APPENGINE_TASKEXECUTIONCOUNT"
_TASK_RETRY_COUNT_HEADER = "HTTP_X_APPENGINE_TASKRETRYCOUNT"
_APPENGINE_CRON_HEADER = "HTTP_X_APPENGINE_CRON"


def task_environment_middleware(get_response):
    def middleware(request):
        # Make sure we set the appengine headers in the environment from the
        # request.
        try:
            _TASK_ENV.task_name = request.META.get(_TASK_NAME_HEADER)
            _TASK_ENV.queue_name = request.META.get(_QUEUE_NAME_HEADER)
            _TASK_ENV.task_execution_count = request.META.get(_TASK_EXECUTION_COUNT_HEADER)
            _TASK_ENV.task_retry_count = request.META.get(_TASK_RETRY_COUNT_HEADER)
            _TASK_ENV.is_cron = bool(request.META.get(_APPENGINE_CRON_HEADER))

            return get_response(request)
        finally:
            for attr in (
                "task_name",
                "queue_name",
                "task_execution_count",
                "task_retry_count"
                "is_cron"
            ):
                setattr(_TASK_ENV, attr, None)

    return middleware


TaskEnvironmentMiddleware = task_environment_middleware
