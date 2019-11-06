from django.db import models


from app.querysets.abstracts import SoftDeletionQuerySet

class SoftDeletionManager(models.Manager):
    def get_queryset(self):
        return SoftDeletionQuerySet(self.model).filter(is_active=True)

    def get_all(self):
        return SoftDeletionQuerySet(self.model).all()
