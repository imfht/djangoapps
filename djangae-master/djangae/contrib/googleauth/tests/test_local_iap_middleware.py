import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http.response import HttpResponse
from django.test.utils import override_settings
from django.urls.conf import path

from djangae.test import TestCase

User = get_user_model()

urlpatterns = [
    path('', lambda request: HttpResponse('Ok'), name='index')
]


@override_settings(ROOT_URLCONF=__name__)
class LocalIAPMiddlewareTests(TestCase):

    def setUp(self):
        super().setUp()
        settings.MIDDLEWARE.insert(
            settings.MIDDLEWARE.index('djangae.contrib.googleauth.middleware.AuthenticationMiddleware'),
            'djangae.contrib.googleauth.middleware.LocalIAPLoginMiddleware'
        )

    def tearDown(self):
        super().tearDown()
        settings.MIDDLEWARE.remove('djangae.contrib.googleauth.middleware.LocalIAPLoginMiddleware')

    def test_login_view_displayed(self):
        response = self.client.get("/_dj/login/")
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertTrue("id_email" in content)

    def test_redirect_on_successful_login(self):
        form_data = {
            "email": "test@example.com"
        }

        response = self.client.post("/_dj/login/?next=/", form_data, follow=True)
        self.assertEqual(response.status_code, 200)

        self.assertIn('_auth_user_id', self.client.session)

        self.assertTrue(
            User.objects.filter(
                email="test@example.com"
            ).exists()
        )

    def test_login_failure(self):
        form_data = {
            "email": "test"
        }

        response = self.client.post("/_dj/login/?next=/", form_data)
        self.assertEqual(response.status_code, 200)

    def test_noop_on_production(self):
        try:
            os.environ['GAE_ENV'] = 'standard'
            response = self.client.get("/_dj/login/")
            self.assertEqual(404, response.status_code)
        finally:
            del os.environ['GAE_ENV']

    def test_logout(self):
        form_data = {
            "email": "test@example.com"
        }

        response = self.client.post(
            "/_dj/logout/?next=/",
            form_data,
            follow=True
        )

        self.assertEqual(response.status_code, 200)
