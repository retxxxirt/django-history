from uuid import uuid4

from django.db import models
from django.utils import timezone

from django_history.fields import RemoteField


class History(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)

    model_name = models.CharField(max_length=256, db_index=True)
    instance_pk = RemoteField(db_index=True)

    field_name = models.CharField(max_length=256, db_index=True)
    field_value = RemoteField(null=True)

    added_at = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ('-added_at',)
