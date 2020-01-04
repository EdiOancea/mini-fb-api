import json

from app.tests.base_test import BaseTestCase
from app.models import User
from app.serializers import UserSerializer

class UserTestCase(BaseTestCase):
    fixtures = ('user',)

    def test_retrieve(self):
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

    def test_retrieve_404(self):
        config = { 'url': '/users/asdaf/' }

        response = self.client.get(
            self.SERVER_NAME + config['url'],
            format='json'
        )

        self.assertEqual(response.status_code, 404)

    def test_retrieve_inactive(self):
        config = { 'url': '/users/2/' }

        response = self.client.get(
            self.SERVER_NAME + config['url'],
            format='json'
        )

        self.assertEqual(response.status_code, 404)

    def test_list(self):
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

    def test_list_all(self):
        config = { 'url': '/users/all/' }

        response = self.client.get(
            self.SERVER_NAME + config['url'],
            format='json'
        )

        self.assertEqual(response.status_code, 200)

        objects = User.objects.get_all()
        data = UserSerializer(objects, many=True).data
        content = json.loads(response.content)

        self.assertEqual(content, data)

    def test_create(self):
        config = {
            'url': '/users/',
            'payload': {
            	'email': 'eduard.oancea_nou@algotech.solutions',
            	'first_name': 'Oancea',
            	'last_name': 'Eduard',
            	'password': '123123',
            	'level': 'regular_user'
            },
        }
        user_no = User.objects.all().count()

        response = self.client.post(
            self.SERVER_NAME + config['url'],
            config['payload'],
            format='json'
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(user_no + 1, User.objects.all().count())

    def test_create_duplicate(self):
        config = {
            'url': '/users/',
            'payload': {
            	'email': 'eduard.oancea@algotech.solutions',
            	'first_name': 'Oancea',
            	'last_name': 'Eduard',
            	'password': '123123',
            	'level': 'regular_user'
            },
        }
        user_no = User.objects.all().count()

        response = self.client.post(
            self.SERVER_NAME + config['url'],
            config['payload'],
            format='json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(user_no, User.objects.all().count())

    def test_update(self):
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

    def test_update_failure(self):
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

    def test_update_404(self):
        config = {
            'url': '/users/motor/',
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

        self.assertEqual(response.status_code, 404)

    def test_delete(self):
        config = { 'url': '/users/1/' }
        user_no = User.objects.all().count()

        response = self.client.delete(
            self.SERVER_NAME + config['url'],
            format='json'
        )

        self.assertEqual(response.status_code, 204)
        self.assertEqual(user_no - 1, User.objects.all().count())

    def test_delete_404(self):
        config = { 'url': '/users/motorulMeu/' }
        user_no = User.objects.all().count()

        response = self.client.delete(
            self.SERVER_NAME + config['url'],
            format='json'
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(user_no, User.objects.all().count())
