from django.test import TestCase
from rest_framework.test import APIClient

from app.models import User


class BaseTestCase(TestCase):
    SERVER_NAME = 'http://testserver.com/api'
    fixutures = ()

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.get(email='eduard.oancea@algotech.solutions')
        self.client.force_authenticate(user=self.user)
