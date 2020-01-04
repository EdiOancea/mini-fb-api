from django.db import models

from app.models.abstracts import Date
from app.models import User, Post

class Comment(Date):
    class Meta:
        db_table = 'comments'

    content = models.TextField()
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
