import unittest
from django.test import Client


class SessionTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
