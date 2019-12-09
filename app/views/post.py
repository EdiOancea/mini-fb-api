from django.http import Http404
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from app.models import Post
from app.serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = (permissions.AllowAny,)
    lookup_field = 'id'

    def get_queryset(self):
        try:
            return Post.objects.filter(user_id=self.kwargs['user_id'])
        except:
            raise Http404('Not found.')
