from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from app.models.abstracts import Date, SoftDeletionModel

class User(AbstractBaseUser, Date, SoftDeletionModel):
    class Meta:
        db_table = 'users'

    REGULAR_USER_LEVEL = 'regular_user'
    SUPER_USER_LEVEL = 'super_user'
    USERNAME_FIELD = 'email'
    
    USER_LEVELS = [
        (REGULAR_USER_LEVEL, 'Regular User'),
        (SUPER_USER_LEVEL, 'Super User'),
    ]

    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)

    level = models.CharField(
        max_length=32,
        default=REGULAR_USER_LEVEL,
        choices=USER_LEVELS
    )

    def get_str_representation(self):
        return {
            'email': self.email,
            'level': self.level,
        }

    def get_full_name(self):
        return self.first_name + self.last_name
