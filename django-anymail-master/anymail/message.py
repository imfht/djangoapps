from email.mime.image import MIMEImage
from email.utils import unquote
import os

from django.core.mail import EmailMessage, EmailMultiAlternatives, make_msgid

from .utils import UNSET


class AnymailMessageMixin(EmailMessage):
    """Mixin for EmailMessage that exposes Anymail features.

    Use of this mixin is optional. You can always just set Anymail
    attributes on any EmailMessage.

    (The mixin can be helpful with type checkers and other development
    tools that complain about accessing Anymail's added attributes
    on a regular EmailMessage.)
    """

    def __init__(self, *args, **kwargs):
        self.esp_extra = kwargs.pop('esp_extra', UNSET)
        self.envelope_sender = kwargs.pop('envelope_sender', UNSET)
        self.metadata = kwargs.pop('metadata', UNSET)
        self.send_at = kwargs.pop('send_at', UNSET)
        self.tags = kwargs.pop('tags', UNSET)
        self.track_clicks = kwargs.pop('track_clicks', UNSET)
        self.track_opens = kwargs.pop('track_opens', UNSET)
        self.template_id = kwargs.pop('template_id', UNSET)
        self.merge_data = kwargs.pop('merge_data', UNSET)
        self.merge_global_data = kwargs.pop('merge_global_data', UNSET)
        self.merge_metadata = kwargs.pop('merge_metadata', UNSET)
        self.anymail_status = AnymailStatus()

        super().__init__(*args, **kwargs)

    def attach_inline_image_file(self, path, subtype=None, idstring="img", domain=None):
        """Add inline image from file path to an EmailMessage, and return its content id"""
        assert isinstance(self, EmailMessage)
        return attach_inline_image_file(self, path, subtype, idstring, domain)

    def attach_inline_image(self, content, filename=None, subtype=None, idstring="img", domain=None):
        """Add inline image and return its content id"""
        assert isinstance(self, EmailMessage)
        return attach_inline_image(self, content, filename, subtype, idstring, domain)


class AnymailMessage(AnymailMessageMixin, EmailMultiAlternatives):
    pass


def attach_inline_image_file(message, path, subtype=None, idstring="img", domain=None):
    """Add inline image from file path to an EmailMessage, and return its content id"""
    filename = os.path.basename(path)
    with open(path, 'rb') as f:
        content = f.read()
    return attach_inline_image(message, content, filename, subtype, idstring, domain)


def attach_inline_image(message, content, filename=None, subtype=None, idstring="img", domain=None):
    """Add inline image to an EmailMessage, and return its content id"""
    if domain is None:
        # Avoid defaulting to hostname that might end in '.com', because some ESPs
        # use Content-ID as filename, and Gmail blocks filenames ending in '.com'.
        domain = 'inline'  # valid domain for a msgid; will never be a real TLD
    content_id = make_msgid(idstring, domain)  # Content ID per RFC 2045 section 7 (with <...>)
    image = MIMEImage(content, subtype)
    image.add_header('Content-Disposition', 'inline', filename=filename)
    image.add_header('Content-ID', content_id)
    message.attach(image)
    return unquote(content_id)  # Without <...>, for use as the <img> tag src


ANYMAIL_STATUSES = [
    'sent',  # the ESP has sent the message (though it may or may not get delivered)
    'queued',  # the ESP will try to send the message later
    'invalid',  # the recipient email was not valid
    'rejected',  # the recipient is blacklisted
    'failed',  # the attempt to send failed for some other reason
    'unknown',  # anything else
]


class AnymailRecipientStatus:
    """Information about an EmailMessage's send status for a single recipient"""

    def __init__(self, message_id, status):
        self.message_id = message_id  # ESP message id
        self.status = status  # one of ANYMAIL_STATUSES, or None for not yet sent to ESP


class AnymailStatus:
    """Information about an EmailMessage's send status for all recipients"""

    def __init__(self):
        self.message_id = None  # set of ESP message ids across all recipients, or bare id if only one, or None
        self.status = None  # set of ANYMAIL_STATUSES across all recipients, or None for not yet sent to ESP
        self.recipients = {}  # per-recipient: { email: AnymailRecipientStatus, ... }
        self.esp_response = None

    def set_recipient_status(self, recipients):
        self.recipients.update(recipients)
        recipient_statuses = self.recipients.values()
        self.message_id = set([recipient.message_id for recipient in recipient_statuses])
        if len(self.message_id) == 1:
            self.message_id = self.message_id.pop()  # de-set-ify if single message_id
        self.status = set([recipient.status for recipient in recipient_statuses])
