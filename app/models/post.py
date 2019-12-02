from django.db import models

from app.models.abstracts import Date
from app.models import User
from app.managers import UserManager

class Post(Date):
    class Meta:
        db_table = 'posts'

    REQUIRED_FIELDS = ['content']

    content = models.TextField()
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    
