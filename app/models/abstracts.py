from django.db import models
from datetime import datetime

from app.managers.abstracts import SoftDeletionManager


class Date(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        abstract = True

class SoftDeletionModel(models.Model):
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = datetime.now()
        self.save()

    def hard_delete(self):
        super(SoftDeletionModel, self).delete()
