# djangae.tasks

The djangae.tasks app provides functionality for working with Google Cloud Tasks from your Django application.

The main functionality it provides is the ability to "defer" a function to be run later by Cloud Tasks. It
also provides a number of helper methods that leverage that ability.

## Google Cloud Tasks Emulator

When developing locally, it is recommended you make use of the [GCloud Tasks Emulator](https://gitlab.com/potato-oss/google-cloud/gcloud-tasks-emulator)
project that simulates the Cloud Task API locally.

Djangae's sandbox.py provides functionality to start/stop the emulator for you, and djangae.tasks integrates with the emulator when it's running.

## djangae.tasks.deferred.defer

The App Engine SDK provides a utility function called `defer()` which is used to call
functions and methods from the task queue.

The built-in `defer()` method suffers from a number of issues with both bugs, and the API itself.

`djangae.deferred.defer` is a near-drop-in replacement for `google.appengine.ext.deferred.defer` with a few differences:

 - The code has been altered to always use a Datastore entity group unless the task is explicitly marked as being "small" (less than 100k) with the `_small_task=True` flag.
 - If a Django instance is passed as an argument to the called function, then the foreign key caches are wiped before
   deferring to avoid bloating and stale data when the task runs. This can be disabled with `_wipe_related_caches=False`
 - Transactional tasks do not *guarantee* that the task will run. It's possible (but unlikely) for the transaction to complete
   successfully, but the queuing of the task to fail. It is not possible for the transaction to fail and the task to queue however.
 - `_transactional` defaults to `True` if called within an atomic() block, or `False` otherwise.
 - `_using` is provided to choose which connection should control transactional queuing. Defaults to "default".

Everything else should behave in the same way.

## djange.tasks.deferred.defer_iteration_with_finalize

`defer_iteration_with_finalize(queryset, callback, finalize, args=None, _queue='default', _shards=5, _delete_marker=True, _transactional=False)`

This function provides similar functionality to a Mapreduce pipeline, but it's entirely self-contained and leverages
defer to process the tasks.

The function iterates the passed Queryset in shards, calling `callback` on each instance. Once all shards complete then
the `finalize` callback is called. If a shard runs for 9.5 minutes, or it hits an unhandled exception it re-defers another shard to continue processing. This
avoids hitting the 10 minute deadline for background tasks.

This means that callbacks should complete **within a maximum of 30 seconds**. Callbacks that take longer than this could cause the iteration to fail,
or, more likely, repeatedly retry running the callback on the same instances.

If `args` is specified, these arguments are passed as positional arguments to both `callback` (after the instance) and `finalize`.

`_shards` is the number of shards to use for processing. If `_delete_marker` is `True` then the Datastore entity that
tracks complete shards is deleted. If you want to keep these (as a log of sorts) then set this to `False`.

`_transactional` and `_queue` work in the same way as `defer()`

### Identifying a task shard

From a shard callback, you can identify the current shard by using the `get_deferred_shard_index()` method:

```
from djangae.deferred import get_deferred_shard_index
shard_index = get_deferred_shard_index()
```

This can be useful when doing things like updating sharded counters.
