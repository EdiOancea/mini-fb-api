from django.http import Http404
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from app.models import Comment
from app.serializers import CommentSerializer
from app.permissions import IsOwnerOrReadOnly

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly,
    )
    lookup_field = 'id'

    def get_queryset(self):
        try:
            return Comment.objects.filter(
                user_id=self.kwargs['user_id'],
                post_id=self.kwargs['post_id']
            )
        except:
            raise Http404('Not found.')
