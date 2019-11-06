from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from app.models.user import User
from app.serializers.user import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @action(detail=False, methods=['get'])
    def all(self, request):
        queryset = User.objects.get_all()
        serializer = UserSerializer(queryset, many=True)

        return Response(serializer.data)

    @action(detail=True, methods=['put'])
    def reactivate(self, request, pk=None):
        queryset = User.objects.get_all()
        user = get_object_or_404(queryset, pk=pk)
        user.undelete()
        serializer = UserSerializer(user)

        return Response(serializer.data)

    def update(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        existingUser = UserSerializer(user)

        return super(UserViewSet, self).update(request, pk)

    def create(self, request):
        createdUser = User.objects.create_user(**request.data)
        serializer = UserSerializer(createdUser)

        return Response(serializer.data)
