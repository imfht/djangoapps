.. _transient-errors:

Handling transient errors
=========================

Applications using Anymail need to be prepared to deal with connectivity issues
and other transient errors from your ESP's API (as with any networked API).

Because Django doesn't have a built-in way to say "try this again in a few moments,"
Anymail doesn't have its own logic to retry network errors. The best way to handle
transient ESP errors depends on your Django project:

* If you already use something like :pypi:`celery` or :pypi:`Django channels <channels>`
  for background task scheduling, that's usually the best choice for handling Anymail sends.
  Queue a task for every send, and wait to mark the task complete until the send succeeds
  (or repeatedly fails, according to whatever logic makes sense for your app).

* Another option is the Pinax :pypi:`django-mailer` package, which queues and automatically
  retries failed sends for any Django EmailBackend, including Anymail. django-mailer maintains
  its send queue in your regular Django DB, which is a simple way to get started but may not
  scale well for very large volumes of outbound email.

In addition to handling connectivity issues, either of these approaches also has the advantage
of moving email sending to a background thread. This is a best practice for sending email from
Django, as it allows your web views to respond faster.
