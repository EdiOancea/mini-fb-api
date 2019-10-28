from django.db import models
from django.db.models.query import QuerySet

class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return QuerySet(self.model).filter(deleted_at=None)

        return QuerySet(self.model)
