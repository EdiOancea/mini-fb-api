from django.db import models
from django.db.models import QuerySet


from app.querysets.abstracts import SoftDeletionQuerySet

class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        queryset = SoftDeletionQuerySet(self.model)

        if self.alive_only:
            return queryset.filter(is_active=True)

        return queryset
