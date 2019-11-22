import json

from django.test import TestCase
from rest_framework.test import APIClient

class UserTestCase(TestCase):
    fixtures = ('user',)
    SERVER_NAME = 'http://gucci.com/api'

    def setUp(self):
        self.client = APIClient()

    def test_auth_success(self):
        config = {
            'url': '/login/',
            'payload' : {
                'email': 'eduard.oancea@algotech.solutions',
                'password': '123123',
            },
        }

        response = self.client.post(
            self.SERVER_NAME + config['url'],
            config['payload'],
            format='json'
        )

        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(len(content['token']), 0)

    def test_auth_failure(self):
        config = {
            'url': '/login/',
            'payload' : {
                'email': 'eduard.oancea@algotech.solutions',
                'password': '123123123',
            },
        }

        response = self.client.post(
            self.SERVER_NAME + config['url'],
            config['payload'],
            format='json'
        )

        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(content['non_field_errors'][0], 'Unable to log in with provided credentials.')
