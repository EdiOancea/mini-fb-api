from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.db.models import Q


class User(AbstractBaseUser):
    class Meta:
        db_table = 'users'

    REGULAR_USER_LEVEL = 'regular_user'
    SUPER_USER_LEVEL = 'super_user'

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

    def __str__(self):
        return str(self.email)
