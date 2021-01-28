from django.core.mail import EmailMultiAlternatives
from django.test import SimpleTestCase
from mock import patch

from anymail.message import attach_inline_image

from .utils import AnymailTestMixin, sample_image_content


class InlineImageTests(AnymailTestMixin, SimpleTestCase):
    def setUp(self):
        self.message = EmailMultiAlternatives()
        super().setUp()

    @patch("email.utils.socket.getfqdn")
    def test_default_domain(self, mock_getfqdn):
        """The default Content-ID domain should *not* use local hostname"""
        # (This avoids problems with ESPs that re-use Content-ID as attachment
        # filename: if the local hostname ends in ".com", you can end up with
        # an inline attachment filename that causes Gmail to reject the message.)
        mock_getfqdn.return_value = "server.example.com"
        cid = attach_inline_image(self.message, sample_image_content())
        self.assertRegex(cid, r"[\w.]+@inline",
                         "Content-ID should be a valid Message-ID, "
                         "but _not_ @server.example.com")

    def test_domain_override(self):
        cid = attach_inline_image(self.message, sample_image_content(),
                                  domain="example.org")
        self.assertRegex(cid, r"[\w.]+@example\.org",
                         "Content-ID should be a valid Message-ID @example.org")
