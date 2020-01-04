import json

from django.test import TestCase
from rest_framework.test import APIClient

from app.tests.base_test import BaseTestCase
from app.models import User, Post
from app.serializers import PostSerializer

class PostTestCase(BaseTestCase):
    fixtures = ('user', 'post')

    def test_retrieve(self):
        config = { 'url': '/users/1/posts/1/', 'pk': 1 }

        response = self.client.get(
            self.SERVER_NAME + config['url'],
            format='json'
        )

        self.assertEqual(response.status_code, 200)

        objects = Post.objects.get(pk=config['pk'])
        data = PostSerializer(objects).data
        content = json.loads(response.content)

        self.assertEqual(content, data)

    def test_retrieve_invalid_user(self):
        config = { 'url': '/users/ketamina/posts/1/' }

        response = self.client.get(
            self.SERVER_NAME + config['url'],
            format='json'
        )

        self.assertEqual(response.status_code, 404)

    def test_retrieve_invalid_post(self):
        config = { 'url': '/users/1/posts/asda/' }

        response = self.client.get(
            self.SERVER_NAME + config['url'],
            format='json'
        )

        self.assertEqual(response.status_code, 404)

    def test_list(self):
        config = { 'url': '/users/1/posts/', 'user_id': 1 }

        response = self.client.get(
            self.SERVER_NAME + config['url'],
            format='json'
        )

        self.assertEqual(response.status_code, 200)

        objects = Post.objects.filter(user_id=config['user_id'])
        data = PostSerializer(objects, many=True).data
        content = json.loads(response.content)

        self.assertEqual(content, data)

    def test_list_invalid_user(self):
        config = { 'url': '/users/ketamina/posts/' }

        response = self.client.get(
            self.SERVER_NAME + config['url'],
            format='json'
        )

        self.assertEqual(response.status_code, 404)

    def test_create(self):
        config = {
            'url': '/users/1/posts/',
            'user_id': 1,
            'payload': {
                'user': 1,
                'content': 'Hai bosulica',
            },
        }
        post_no = Post.objects.filter(user_id=config['user_id']).count()

        response = self.client.post(
            self.SERVER_NAME + config['url'],
            config['payload'],
            format='json'
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(post_no + 1, Post.objects.filter(user_id=config['user_id']).count())

    def test_create_inexistent_user(self):
        #should return 400
        config = {
            'url': '/users/20/posts/',
            'payload': {
                'user': 20,
                'content': 'Hai bosulica',
            },
        }

        response = self.client.post(
            self.SERVER_NAME + config['url'],
            config['payload'],
            format='json'
        )

        self.assertEqual(response.status_code, 403)

    def test_create_invalid_post(self):
        config = {
            'url': '/users/1/posts/',
            'payload': {
                'user': 1,
                'content': '',
            },
        }

        response = self.client.post(
            self.SERVER_NAME + config['url'],
            config['payload'],
            format='json'
        )

        self.assertEqual(response.status_code, 400)

    def test_update(self):
        config = {
            'url': '/users/1/posts/1/',
            'pk': 1,
            'payload': {
                'id': 1,
                'user': 1,
                'content': 'Hai bosulica',
            },
        }

        response = self.client.put(
            self.SERVER_NAME + config['url'],
            config['payload'],
            format='json'
        )
        serializer = PostSerializer(Post.objects.get(pk=config['pk']))

        self.assertEqual(response.status_code, 200)

        for key, value in config['payload'].items():
            self.assertEqual(value, serializer.data[key])

    def test_update_unallowed(self):
        config = {
            'url': '/users/4/posts/5/',
            'payload': {
                'id': 5,
                'user': 4,
                'content': 'Hai bosulica',
            },
        }

        response = self.client.put(
            self.SERVER_NAME + config['url'],
            config['payload'],
            format='json'
        )

        self.assertEqual(response.status_code, 403)

    def test_update_inexistent_user(self):
        config = { 'url': '/users/20/posts/1/' }

        response = self.client.put(
            self.SERVER_NAME + config['url'],
            {
                'id': 1,
                'content': 'Hai bosulica',
            },
            format='json'
        )

        self.assertEqual(response.status_code, 404)

    def test_update_inexistent_post(self):
        config = { 'url': '/users/1/posts/30/' }

        response = self.client.put(
            self.SERVER_NAME + config['url'],
            {
                'id': 30,
                'content': 'Hai bosulica',
            },
            format='json'
        )

        self.assertEqual(response.status_code, 404)

    def test_delete(self):
        config = { 'url': '/users/1/posts/1/' }
        user_no = Post.objects.filter(user_id=1).count()

        response = self.client.delete(
            self.SERVER_NAME + config['url'],
            format='json'
        )

        self.assertEqual(response.status_code, 204)
        self.assertEqual(user_no - 1, Post.objects.filter(user_id=1).count())

    def test_delete_invalid_user(self):
        config = { 'url': '/users/123/posts/1/' }
        post_no = Post.objects.filter(user_id=1).count()

        response = self.client.delete(
            self.SERVER_NAME + config['url'],
            format='json'
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(post_no, Post.objects.filter(user_id=1).count())

    def test_delete_invalid_post(self):
        config = { 'url': '/users/1/posts/1100/' }
        post_no = Post.objects.filter(user_id=1100).count()

        response = self.client.delete(
            self.SERVER_NAME + config['url'],
            format='json'
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(post_no, Post.objects.filter(user_id=1100).count())
