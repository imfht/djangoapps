# Local/remote management commands

If you set your manage.py up as described [in Installation](installation.md), Djangae will allow you to run management commands locally or remotely.

## Running Commands Locally

Django management commands run as normal, e.g.


    ./manage.py shell


# Local Server Port Configuration

When you call `runserver` the following ports are used by default:

 - The default module (the main webserver) runs on port 8000
 - Additional modules (defined by the `DJANGAE_ADDITIONAL_MODULES` setting) will use sequential ports from 8001
 - The API server runs at port 8010
 - The admin server runs at port 8011
 - The blobstore service (which is used for uploads locally) runs on port 8012

If you override the base port (e.g. `./manage.py runserver localhost:9000`) then additional modules will use sequential
ports from 9001+. The admin, api and blobstore ports will remain the same.

If any ports are found to be in use, the port number will be incremented until a free one is found.

# Additional modules

App Engine apps can be made up of multiple modules (the default being the one defined by app.yaml). If your
project makes use of additional modules then you can specify a list of yaml file paths in the `DJANGAE_ADDITIONAL_MODULES`
and these will be forwarded to the dev_appserver when `runserver` is called

## Running Commands Remotely

Djangae also lets you run management commands which connect remotely to the Datastore of your deployed App Engine application.  To do this you need to:

Add the `remote_api` built-in to app.yaml, and deploy that change.

    builtins:
      - remote_api: on

You also need to ensure that the `application` in app.yaml is set to the application which you wish to connect to.

Then run your management command specifying the `remote` sandbox.

    ./manage.py --sandbox=remote shell

This will use your **local** Python code, but all database operations will be performed on the remote Datastore.

Additionally, you can specify the application to run commands against by providing an `--app_id`. Eg

  ./manage.py --sandbox=remote --app_id=myapp shell  # Starts a remote shell with the "myapp" instance


### Deferring Tasks Remotely

App Engine tasks are stored in the Datastore, so when you are in the remote shell any tasks that you defer will run on the live application, not locally.  For example:

    ./manage.py --sandbox=remote shell
    >>> from my_code import my_function
    >>> from google.appengine.ext.deferred import defer
    >>> defer(my_function, arg1, arg2, _queue="queue_name")


# Testing

Along with the local/remote sandboxes, Djangae ships with a test sandbox. This should be called explicitly
from your manage.py when tests are being run. This sandbox sets up the bare minimum to use the Datastore
connector (the memcache and Datastore stubs only). This prevents accesses to the Datastore from throwing an error
when you do so outside a test case (e.g. from `settings.py`).

Your tests should setup and teardown a full testbed instance (see `DjangaeDiscoverRunner` and the nose plugin).
