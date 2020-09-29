import requests

from django.test import LiveServerTestCase


class IsabotHomepageTest(LiveServerTestCase):
    def test_homepage_is_callable(self):
        url = f"{self.live_server_url}/"
        response = requests.get(url)

        self.assertEqual(200, response.status_code)
        self.assertTrue(response.content.startswith(b"\n\n<html"))

    def test_other_urls_are_redirected(self):
        url = f"{self.live_server_url}/otherurl/"
        response = requests.get(url)

        self.assertEqual(200, response.status_code)
        self.assertTrue(response.content.startswith(b"\n\n<html"))
