from rest_framework import serializers

from app.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['content', 'user', 'id']
        read_only_fields = ['id']
