from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from app.models.user import User
from app.serializers.user import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)

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

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_user = User.objects.create_user(**request.data)

        return Response(serializer.data, status=201)
