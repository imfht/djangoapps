# Environment

Djangae contains a small collection of utility functions which are useful on App Engine.

## Retry

This is a helper for calling functions which may intermittently throw errors.
It is useful for things such as performing Datastore transactions which may collide, or calling other APIs which may occasionally fail but that should succeed on a subsequent attempt.

### `djangae.utils.retry`

```python
retry(function, _catch=None, _attempts=3, _initial_wait=375, _max_wait=30000, _avoid_clashes=True)
```

Calls the given function, catching the given exception(s), and (re)trying up to a maximum of `_attempts` times.
If the intial call fails, it will wait `_initial_wait` milliseconds before making the second attempt.
The wait will double on each subsequent retry, up to a maximum of `_max_wait` milliseconds.

`_catch` defaults to:

```python
(
    djangae.db.transaction.TransactionFailedError,
	google.appengine.api.datastore_errors.Error,
	google.appengine.runtime.apiproxy_errors.Error
)
```

If `_avoid_clashes` is True (default) then a random time up to a second will be added after the first
retry (the retry time is still capped at `_max_wait`). This is to help avoid situations where several
tasks collide, and then all back off for the same amount of time before clashing again.

### `djangae.utils.retry_on_error`

A function decorator which routes the function through `retry`.

```python
@retry_on_error(_catch=None, _attempts=3, _initial_wait=375, _max_wait=30000)
def my_function():
    ...
```

### `djangae.utils.retry_until_successful`

```pythonn
retry(function, _catch=None, _attempts=∞, _initial_wait=375, _max_wait=30000)
```

The same as `retry`, but `_attempts` is unlimited, so it will keep on retrying until either it succeeds or you hit an uncaught exception, such as the App Engine `DeadlineExceededError`.
