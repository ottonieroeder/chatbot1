import unittest
from django.test import Client


class IsabotAPITest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_isabot_api_200(self):
        response = self.client.post(
            "/api/isabot/", {"text": ""}, content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)

    def test_isabot_api_returns_400_if_no_text_is_provided(self):
        response = self.client.post("/api/isabot/", content_type="application/json")

        self.assertEqual(response.status_code, 400)
