.. _anymail-exceptions:

Exceptions
----------

.. module:: anymail.exceptions

.. exception:: AnymailUnsupportedFeature

    If the email tries to use features that aren't supported by the ESP, the send
    call will raise an :exc:`!AnymailUnsupportedFeature` error, and the message
    won't be sent. See :ref:`unsupported-features`.

    You can disable this exception (ignoring the unsupported features and
    sending the message anyway, without them) by setting
    :setting:`ANYMAIL_IGNORE_UNSUPPORTED_FEATURES` to `True`.


.. exception:: AnymailRecipientsRefused

    Raised when *all* recipients (to, cc, bcc) of a message are invalid or rejected by
    your ESP *at send time.* See :ref:`recipients-refused`.

    You can disable this exception by setting :setting:`ANYMAIL_IGNORE_RECIPIENT_STATUS`
    to `True` in your settings.py, which will cause Anymail to treat any
    non-:exc:`AnymailAPIError` response from your ESP as a successful send.


.. exception:: AnymailAPIError

    If the ESP's API fails or returns an error response, the send call will
    raise an :exc:`!AnymailAPIError`.

    The exception's :attr:`status_code` and :attr:`response` attributes may
    help explain what went wrong. (Tip: you may also be able to check the API log in
    your ESP's dashboard. See :ref:`troubleshooting`.)

    In production, it's not unusual for sends to occasionally fail due to transient
    connectivity problems, ESP maintenance, or other operational issues. Typically
    these failures have a 5xx :attr:`status_code`. See :ref:`transient-errors`
    for suggestions on retrying these failed sends.


.. exception:: AnymailInvalidAddress

    .. versionadded:: 0.7

    The send call will raise a :exc:`!AnymailInvalidAddress` error if you
    attempt to send a message with invalidly-formatted email addresses in
    the :attr:`from_email` or recipient lists.

    One source of this error can be using a display-name ("real name") containing
    commas or parentheses. Per :rfc:`5322`, you should use double quotes around
    the display-name portion of an email address:

    .. code-block:: python

        # won't work:
        send_mail(from_email='Widgets, Inc. <widgets@example.com>', ...)
        # must use double quotes around display-name containing comma:
        send_mail(from_email='"Widgets, Inc." <widgets@example.com>', ...)


.. exception:: AnymailSerializationError

    The send call will raise a :exc:`!AnymailSerializationError`
    if there are message attributes Anymail doesn't know how to represent
    to your ESP.

    The most common cause of this error is including values other than
    strings and numbers in your :attr:`merge_data` or :attr:`metadata`.
    (E.g., you need to format `Decimal` and `date` data to
    strings before setting them into :attr:`merge_data`.)

    See :ref:`formatting-merge-data` for more information.
