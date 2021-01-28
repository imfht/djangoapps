.. _django-templates:

Using Django templates for email
================================

ESP's templating languages and merge capabilities are generally not compatible
with each other, which can make it hard to move email templates between them.

But since you're working in Django, you already have access to the
extremely-full-featured :doc:`Django templating system <django:topics/templates>`.
You don't even have to use Django's template syntax: it supports other
template languages (like Jinja2).

You're probably already using Django's templating system for your HTML pages,
so it can be an easy decision to use it for your email, too.

To compose email using *Django* templates, you can use Django's
:func:`~django.template.loader.render_to_string`
template shortcut to build the body and html.

Example that builds an email from the templates ``message_subject.txt``,
``message_body.txt`` and ``message_body.html``:

.. code-block:: python

    from django.core.mail import EmailMultiAlternatives
    from django.template.loader import render_to_string

    merge_data = {
        'ORDERNO': "12345", 'TRACKINGNO': "1Z987"
    }

    subject = render_to_string("message_subject.txt", merge_data).strip()
    text_body = render_to_string("message_body.txt", merge_data)
    html_body = render_to_string("message_body.html", merge_data)

    msg = EmailMultiAlternatives(subject=subject, from_email="store@example.com",
                                 to=["customer@example.com"], body=text_body)
    msg.attach_alternative(html_body, "text/html")
    msg.send()

Tip: use Django's :ttag:`{% autoescape off %}<autoescape>` template tag in your
plaintext ``.txt`` templates to avoid inappropriate HTML escaping.


Helpful add-ons
---------------

These (third-party) packages can be helpful for building your email
in Django:

* :pypi:`django-templated-mail`, :pypi:`django-mail-templated`, or :pypi:`django-mail-templated-simple`
  for building messages from sets of Django templates.
* :pypi:`premailer` for inlining css before sending
* :pypi:`BeautifulSoup`, :pypi:`lxml`, or :pypi:`html2text` for auto-generating plaintext from your html
