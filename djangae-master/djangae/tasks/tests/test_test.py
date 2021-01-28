from djangae.tasks import deferred
from djangae.test import TestCase, TaskFailedBehaviour, TaskFailedError


def my_task():
    """
    Basic task for testing task queues.
    """
    pass


def throw_once():
    throw_once.counter += 1
    if throw_once.counter == 1:
        raise Exception("First call")


throw_once.counter = 0


class TaskQueueTests(TestCase):

    def test_get_task_count(self):
        deferred.defer(my_task)
        deferred.defer(my_task, _queue='another')

        # We don't use self.assertNumTasksEquals here because we want to flush.
        task_count = self.get_task_count("default")
        self.assertEqual(1, task_count)

        task_count = self.get_task_count("another")
        self.assertEqual(1, task_count)

    def test_task_queue_processing_control(self):

        deferred.defer(throw_once)

        self.process_task_queues(failure_behaviour=TaskFailedBehaviour.RETRY_TASK)

        # Should've retried
        self.assertEqual(throw_once.counter, 2)

        throw_once.counter = 0

        deferred.defer(throw_once)

        self.assertRaises(
            TaskFailedError,
            self.process_task_queues,
            failure_behaviour=TaskFailedBehaviour.RAISE_ERROR
        )
        self.assertEqual(throw_once.counter, 1)
