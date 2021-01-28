import os

from djangae.environment import (
    is_development_environment,
    is_production_environment,
)
from djangae.test import TestCase


class EnvironmentUtilsTest(TestCase):

    def test_is_production_environment(self):
        self.assertFalse(is_production_environment())
        os.environ["GAE_ENV"] = 'standard'
        self.assertTrue(is_production_environment())
        del os.environ["GAE_ENV"]

    def test_is_development_environment(self):
        self.assertTrue(is_development_environment())
        os.environ["GAE_ENV"] = 'standard'
        self.assertFalse(is_development_environment())
        del os.environ["GAE_ENV"]
