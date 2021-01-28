# STANDARD LIB
import logging

# THIRD PARTY
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone


# DJANGAE
from .models import DatastoreLock

logger = logging.getLogger(__name__)


# GAE background tasks and crons can run for a maximum of 10 minutes, so in theory you shouldn't
# be locking a block of code which takes longer than that, and even if you're using backends which
# can run for longer, you would still be mad to lock a block of code which runs for > 10 minutes
DELETE_LOCKS_OLDER_THAN_SECONDS = 600
QUEUE = getattr(settings, 'DJANGAE_CLEANUP_LOCKS_QUEUE', 'default')


def cleanup_locks(request):
    """ Delete all Lock objects that are older than 10 minutes. """

    from djangae.tasks.deferred import defer

    logger.info("Deferring djangae.contrib.lock cleanup task")
    defer(cleanup_locks_task, _queue=QUEUE)
    return HttpResponse("Cleanup locks task is running")


def cleanup_locks_task():
    """ Task function that deletes lock objects that are older than 10 minutes.
        Due to its restriction of not being able to use an inequality filter, we can' use
        defer_iteration for this, but if we can't delete all the objects in this one task then it
        will just fail and retry, and everntually it will get through all of them.
    """
    logger.info("Starting djangae.contrib.lock cleanup task")
    cut_off = timezone.now() - timezone.timedelta(seconds=DELETE_LOCKS_OLDER_THAN_SECONDS)
    queryset = DatastoreLock.objects.filter(timestamp__lt=cut_off)
    queryset.delete()
    logger.info("Finished djangae.contrib.lock cleanup task")


def _delete_lock(lock):
    logger.info("Deleting stale lock '%s' with timestamp %r", lock.identifier, lock.timestamp)
    lock.delete()
