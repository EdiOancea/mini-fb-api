from django.http import Http404
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from app.models.user import User
from app.serializers.user import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    lookup_field = 'id'

    @action(detail=False, methods=['get'])
    def all(self, request):
        queryset = User.objects.get_all()
        serializer = UserSerializer(queryset, many=True)

        return Response(serializer.data)

    @action(detail=True, methods=['put'])
    def reactivate(self, request, id=None):
        try:
            user = User.objects.filter(pk=id)
            user.undelete()
            serializer = UserSerializer(user)

            return Response(serializer.data)
        except:
            raise Http404('Not found.')

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_user = User.objects.create_user(**request.data)

        return Response(UserSerializer(instance=create_user).data, status=201)
