import json

from django.test import TestCase
from django.http import HttpRequest
from rest_framework.test import APIClient

from app.models import User
from app.serializers import UserSerializer

class UserTestCase(TestCase):
    fixtures = ('user',)
    SERVER_NAME = 'http://gucci.com/api'

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.get(email='eduard.oancea@algotech.solutions')
        self.client.force_authenticate(user=self.user)

    def test_get_one(self):
        config = { 'url': '/users/1/', 'pk': 1}

        response = self.client.get(
            self.SERVER_NAME + config['url'],
            format='json'
        )

        self.assertEqual(response.status_code, 200)

        object = User.objects.get(pk=config['pk'])
        data = UserSerializer(object).data
        content = json.loads(response.content)

        self.assertEqual(content, data)

    def test_get_one_inactive(self):
        config = { 'url': '/users/2/', 'pk': 2}

        response = self.client.get(
            self.SERVER_NAME + config['url'],
            format='json'
        )

        self.assertEqual(response.status_code, 404)

    def test_get_all(self):
        config = { 'url': '/users/' }

        response = self.client.get(
            self.SERVER_NAME + config['url'],
            format='json'
        )

        self.assertEqual(response.status_code, 200)

        objects = User.objects.all()
        data = UserSerializer(objects, many=True).data
        content = json.loads(response.content)

        self.assertEqual(content, data)

    def test_get_all_with_inactive(self):
        config = { 'url': '/users/all/' }

        response = self.client.get(
            self.SERVER_NAME + config['url'],
            format='json'
        )

        self.assertEqual(response.status_code, 200)

    def test_create_success(self):
        config = { 'url': '/users/' }
        user_no = User.objects.all().count()

        response = self.client.post(
            self.SERVER_NAME + config['url'],
            {
            	'email': 'eduard.oancea_nou@algotech.solutions',
            	'first_name': 'Oancea',
            	'last_name': 'Eduard',
            	'password': '123123',
            	'level': 'regular_user'
            },
            format='json'
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(user_no + 1, User.objects.all().count())

    def test_create_duplicate(self):
        config = { 'url': '/users/' }
        user_no = User.objects.all().count()

        response = self.client.post(
            self.SERVER_NAME + config['url'],
            {
            	'email': 'eduard.oancea@algotech.solutions',
            	'first_name': 'Oancea',
            	'last_name': 'Eduard',
            	'password': '123123',
            	'level': 'regular_user'
            },
            format='json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(user_no, User.objects.all().count())

    def test_put_success(self):
        config = {
            'url': '/users/1/',
            'pk': '1',
            'payload': {
                'first_name': 'Oancea',
                'last_name': 'Eduarda',
                'level': 'super_user',
                'email': 'oof@oof.ro',
            },
        }

        response = self.client.put(
            self.SERVER_NAME + config['url'],
            config['payload'],
            format='json'
        )
        serializer = UserSerializer(User.objects.get(pk=config['pk']))

        self.assertEqual(response.status_code, 200)
        for key, value in config['payload'].items():
            self.assertEqual(value, serializer.data[key])

    def test_put_failure(self):
        config = {
            'url': '/users/1/',
            'pk': '1',
            'payload': {
                'first_name': 'Oancea',
                'last_name': '',
                'level': 'super_user',
                'email': 'oof@oof.ro',
            },
        }

        response = self.client.put(
            self.SERVER_NAME + config['url'],
            config['payload'],
            format='json'
        )

        self.assertEqual(response.status_code, 400)

    def test_delete_success(self):
        config = {
            'url': '/users/1/',
            'pk': '1',
        }
        user_no = User.objects.all().count()

        response = self.client.delete(
            self.SERVER_NAME + config['url'],
            format='json'
        )

        self.assertEqual(response.status_code, 204)
        self.assertEqual(user_no - 1, User.objects.all().count())

    def test_delete_failure(self):
        config = {
            'url': '/users/100/',
            'pk': '100',
        }
        user_no = User.objects.all().count()

        response = self.client.delete(
            self.SERVER_NAME + config['url'],
            format='json'
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(user_no, User.objects.all().count())
