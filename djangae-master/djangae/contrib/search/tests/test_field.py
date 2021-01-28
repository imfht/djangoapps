from djangae.test import TestCase
from ..fields import Field


class fieldTestCase(TestCase):
    def test_clean_token_trailing_plus(self):
        field = Field()
        token = "a+"
        cleaned_token = field.clean_token(token)
        self.assertEqual(token, cleaned_token)

    def test_clean_token_plus_in_word(self):
        field = Field()
        token = "a+a"
        cleaned_token = field.clean_token(token)
        self.assertEqual('aa', cleaned_token)

    def test_clean_token_only_plusses(self):
        field = Field()
        token = "++"
        cleaned_token = field.clean_token(token)
        self.assertEqual(token, cleaned_token)
