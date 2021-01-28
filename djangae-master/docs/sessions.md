# Django Sessions

## Clearing Sessions

You cannot run a management command to clear django sessions on appengine, djangae has an endpoint which takes care of this. A recommended solution is to add a task to [cron.yaml](https://cloud.google.com/appengine/docs/python/config/cron).

    - description: clear sessions
      url: /_ah/clearsessions
      schedule: every 24 hours

The clearsessions view is restricted to tasks and admins only