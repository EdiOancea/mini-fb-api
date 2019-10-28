from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from app.models.user import User
from app.serializers.user import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
