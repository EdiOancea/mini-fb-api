from django.contrib.auth.models import BaseUserManager

from app.managers.abstracts import SoftDeletionManager


class UserManager(SoftDeletionManager, BaseUserManager):
    def create_user(self, *args, **kwargs):
        user = self.model(
            first_name=kwargs['first_name'],
            last_name=kwargs['last_name'],
            email=self.normalize_email(kwargs['email']),
            level=kwargs['level'],
        )

        user.set_password(kwargs['password'])
        user.save(using=self._db)

        return user
