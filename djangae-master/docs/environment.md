# djangae.environment

You can detect things about your running environment by using the utility functions
located in djangae.environment, and djangae.tasks.environment

## djangae.environment.is_production_environment()

Returns if the request is currently running on the live GAE servers

## djangae.environment.is_development_environment()

Returns whether or not the code is running on the local development environment

## djangae.environment.application_id()

Returns the application id from app.yaml (or wherever the code is deployed)

## djangae.environment.get_application_root()

Returns the root folder of your application (this is the folder containing app.yaml)


# djangae.tasks.environment

For the task-specific environment functions and decorators to work, you must add `djangae.tasks.middleware.TaskEnvironmentMiddleware` to your `MIDDLEWARE` setting.

## djangae.environment.task_name()

Returns the current task name if the code is running on a task queue

## djangae.environment.task_queue_name()

Returns the current task queue name if the code is running on a task queue

## djangae.environment.is_in_task()

Returns true if the code is running in a task on the task queue

## djangae.environment.task_retry_count()

Returns the number of times the task has retried, or 0 if the code is not
running on a queue

# Decorators

## djangae.decorators.task_only

View decorator to allow restricting views to tasks (including crons) or admins of the application.

## djangae.decorators.task_or_superuser_only

View decorator that allows through tasks, or users with `is_superuser == True`

## djangae.decorators.csrf_except_if_task

View decorator that marks the view csrf_exempt *only* if it's being requested by Cloud Tasks
