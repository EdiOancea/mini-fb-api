from django.db.models import QuerySet


class SoftDeletionQuerySet(QuerySet):
    def delete(self):
        return super(SofttDeletionQuerySet, self).update(is_active=False)

    def hard_delete(self):
        return super(SoftDeletionQuerySet, self).delete()

    def alive(self):
        return self.filter(is_active=True)

    def dead(self):
        return self.filter(is_active=False)
