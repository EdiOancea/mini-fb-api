from rest_framework import serializers

from app.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content', 'user', 'post','id']
        read_only_fields = ['id']
