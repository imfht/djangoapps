.. currentmodule:: anymail.message

.. _templates-and-merge:

Batch sending/merge and ESP templates
=====================================

If your ESP offers templates and batch-sending/merge capabilities,
Anymail can simplify using them in a portable way. Anymail doesn't
translate template syntax between ESPs, but it does normalize using
templates and providing merge data for batch sends.

Here's an example using both an ESP stored template and merge data:

.. code-block:: python

    from django.core.mail import EmailMessage

    message = EmailMessage(
        subject=None,  # use the subject in our stored template
        from_email="marketing@example.com",
        to=["Wile E. <wile@example.com>", "rr@example.com"])
    message.template_id = "after_sale_followup_offer"  # use this ESP stored template
    message.merge_data = {  # per-recipient data to merge into the template
        'wile@example.com': {'NAME': "Wile E.",
                             'OFFER': "15% off anvils"},
        'rr@example.com':   {'NAME': "Mr. Runner"},
    }
    message.merge_global_data = {  # merge data for all recipients
        'PARTNER': "Acme, Inc.",
        'OFFER': "5% off any Acme product",  # a default if OFFER missing for recipient
    }
    message.send()

The message's :attr:`~AnymailMessage.template_id` identifies a template stored
at your ESP which provides the message body and subject. (Assuming the
ESP supports those features.)

The message's :attr:`~AnymailMessage.merge_data` supplies the per-recipient
data to substitute for merge fields in your template. Setting this attribute
also lets Anymail know it should use the ESP's :ref:`batch sending <batch-send>`
feature to deliver separate, individually-customized messages
to each address on the "to" list. (Again, assuming your ESP
supports that.)

.. note::

    Templates and batch sending capabilities can vary widely
    between ESPs, as can the syntax for merge fields. Be sure
    to read the notes for :ref:`your specific ESP <supported-esps>`,
    and test carefully with a small recipient list before
    launching a gigantic batch send.

Although related and often used together, :ref:`esp-stored-templates`
and :ref:`merge data <merge-data>` are actually independent features.
For example, some ESPs will let you use merge field syntax
directly in your :class:`~django.core.mail.EmailMessage`
body, so you can do customized batch sending without needing
to define a stored template at the ESP.


.. _esp-stored-templates:

ESP stored templates
--------------------

Many ESPs support transactional email templates that are stored and
managed within your ESP account. To use an ESP stored template
with Anymail, set :attr:`~AnymailMessage.template_id`
on an :class:`~django.core.mail.EmailMessage`.

.. attribute:: AnymailMessage.template_id

    The identifier of the ESP stored template you want to use.
    For most ESPs, this is a `str` name or unique id.
    (See the notes for your :ref:`specific ESP <supported-esps>`.)

    .. code-block:: python

        message.template_id = "after_sale_followup_offer"

With most ESPs, using a stored template will ignore any
body (plain-text or HTML) from the :class:`~django.core.mail.EmailMessage`
object.

A few ESPs also allow you to define the message's subject as part of the template,
but any subject you set on the :class:`~django.core.mail.EmailMessage`
will override the template subject. To use the subject stored with the ESP template,
set the message's `subject` to `None`:

    .. code-block:: python

        message.subject = None  # use subject from template (if supported)

Similarly, some ESPs can also specify the "from" address in the template
definition. Set `message.from_email = None` to use the template's "from."
(You must set this attribute *after* constructing an
:class:`~django.core.mail.EmailMessage` object; passing
`from_email=None` to the constructor will use Django's
:setting:`DEFAULT_FROM_EMAIL` setting, overriding your template value.)


.. _batch-send:
.. _merge-data:

Batch sending with merge data
-----------------------------

Several ESPs support "batch transactional sending," where a single API call can send messages
to multiple recipients. The message is customized for each email on the "to" list
by merging per-recipient data into the body and other message fields.

To use batch sending with Anymail (for ESPs that support it):

* Use "merge fields" (sometimes called "substitution variables" or similar)
  in your message. This could be in an :ref:`ESP stored template <esp-stored-templates>`
  referenced by :attr:`~AnymailMessage.template_id`,
  or with some ESPs you can use merge fields directly in your
  :class:`~django.core.mail.EmailMessage` (meaning the message itself
  is treated as an on-the-fly template).
* Set the message's :attr:`~AnymailMessage.merge_data` attribute to define merge field
  substitutions for each recipient, and optionally set :attr:`~AnymailMessage.merge_global_data`
  to defaults or values to use for all recipients.
* Specify all of the recipients for the batch in the message's `to` list.

.. caution::

    It's critical to set the :attr:`~AnymailMessage.merge_data`
    (or :attr:`~AnymailMessage.merge_metadata`) attribute:
    this is how Anymail recognizes the message as a batch send.

    When you provide merge_data, Anymail will tell the ESP to send an individual customized
    message to each "to" address. Without it, you may get a single message to everyone,
    exposing all of the email addresses to all recipients.
    (If you don't have any per-recipient customizations, but still want individual messages,
    just set merge_data to an empty dict.)

The exact syntax for merge fields varies by ESP. It might be something like
`*|NAME|*` or `-name-` or `<%name%>`. (Check the notes for
:ref:`your ESP <supported-esps>`, and remember you'll need to change
the template if you later switch ESPs.)


.. attribute:: AnymailMessage.merge_data

    A `dict` of *per-recipient* template substitution/merge data. Each key in the
    dict is a recipient email address, and its value is a `dict` of merge field
    names and values to use for that recipient:

    .. code-block:: python

        message.merge_data = {
            'wile@example.com': {'NAME': "Wile E.",
                                 'OFFER': "15% off anvils"},
            'rr@example.com':   {'NAME': "Mr. Runner",
                                 'OFFER': "instant tunnel paint"},
        }

    When `merge_data` is set, Anymail will use the ESP's batch sending option,
    so that each `to` recipient gets an individual message (and doesn't see the
    other emails on the `to` list).

.. attribute:: AnymailMessage.merge_global_data

    A `dict` of template substitution/merge data to use for *all* recipients.
    Keys are merge field names in your message template:

    .. code-block:: python

        message.merge_global_data = {
            'PARTNER': "Acme, Inc.",
            'OFFER': "5% off any Acme product",  # a default OFFER
        }

Merge data values must be strings. (Some ESPs also allow other
JSON-serializable types like lists or dicts.)
See :ref:`formatting-merge-data` for more information.

Like all :ref:`anymail-send-features`, you can use these extended template and
merge attributes with any :class:`~django.core.mail.EmailMessage` or subclass object.
(It doesn't have to be an :class:`AnymailMessage`.)

Tip: you can add :attr:`~!AnymailMessage.merge_global_data` to your
global Anymail :ref:`send defaults <send-defaults>` to supply merge data
available to all batch sends (e.g, site name, contact info). The global
defaults will be merged with any per-message :attr:`~!AnymailMessage.merge_global_data`.


.. _formatting-merge-data:

Formatting merge data
---------------------

If you're using a `date`, `datetime`, `Decimal`, or anything other
than strings and integers, you'll need to format them into strings
for use as merge data:

.. code-block:: python

    product = Product.objects.get(123)  # A Django model
    total_cost = Decimal('19.99')
    ship_date = date(2015, 11, 18)

    # Won't work -- you'll get "not JSON serializable" errors at send time:
    message.merge_global_data = {
        'PRODUCT': product,
        'TOTAL_COST': total_cost,
        'SHIP_DATE': ship_date
    }

    # Do something this instead:
    message.merge_global_data = {
        'PRODUCT': product.name,  # assuming name is a CharField
        'TOTAL_COST': "{cost:0.2f}".format(cost=total_cost),
        'SHIP_DATE': ship_date.strftime('%B %d, %Y')  # US-style "March 15, 2015"
    }

These are just examples. You'll need to determine the best way to format
your merge data as strings.

Although floats are usually allowed in merge data, you'll generally want to format them
into strings yourself to avoid surprises with floating-point precision.

Anymail will raise :exc:`~anymail.exceptions.AnymailSerializationError` if you attempt
to send a message with merge data (or metadata) that can't be sent to your ESP.


ESP templates vs. Django templates
----------------------------------

ESP templating languages are generally proprietary,
which makes them inherently non-portable.

Anymail only exposes the stored template capabilities that your ESP
already offers, and then simplifies providing merge data in a portable way.
It won't translate between different ESP template syntaxes, and it
can't do a batch send if your ESP doesn't support it.

There are two common cases where ESP template
and merge features are particularly useful with Anymail:

* When the people who develop and maintain your transactional
  email templates are different from the people who maintain
  your Django page templates. (For example, you use a single
  ESP for both marketing and transactional email, and your
  marketing team manages all the ESP email templates.)

* When you want to use your ESP's batch-sending capabilities
  for performance reasons, where a single API call can
  trigger individualized messages to hundreds or thousands of recipients.
  (For example, sending a daily batch of shipping notifications.)

If neither of these cases apply, you may find that
:ref:`using Django templates <django-templates>` can be a more
portable and maintainable approach for building transactional email.
