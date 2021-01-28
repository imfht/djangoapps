import logging

from djangae.test import TestCase
from djangae.contrib.security.management.commands import dumpurls
from djangae.contrib.security.middleware import (
    get_default_argument,
    find_argument_index,
    replace_default_argument
)


class DumpUrlsTests(TestCase):
    def test_dumpurls(self):
        """ Test that the `dumpurls` command runs without dying. """
        logging.debug('%s', "*" * 50)
        command = dumpurls.Command()
        command.handle()


class MiddlewareTests(TestCase):

    def test_find_argument_index(self):
        def dummy(a, b):
            pass

        self.assertEqual(find_argument_index(dummy, 'b'), 1)

    def test_get_default_argument(self):
        def dummy(a, b=2):
            pass

        self.assertEqual(get_default_argument(dummy, 'b'), 2)

    def test_replace_default_argument(self):
        def dummy(a, b=2):
            pass

        replace_default_argument(dummy, 'b', 5)
        self.assertEqual(get_default_argument(dummy, 'b'), 5)
