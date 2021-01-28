from djangae.test import TestCase
from django.urls import reverse


class ViewsTests(TestCase):
    def test_clearsessions(self):
        response = self.client.post(reverse("clearsessions"))
        self.assertEqual(response.status_code, 403)

        response = self.client.post(reverse("clearsessions"), HTTP_X_APPENGINE_CRON="1")
        self.assertEqual(response.status_code, 200)
