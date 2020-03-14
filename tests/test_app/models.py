from uuid import uuid4

from django.db import models
from django.utils import timezone

from django_history.managers import HistoryManager


class ModelA(models.Model):
    int_field = models.IntegerField()
    str_field = models.CharField(max_length=256)
    date_field = models.DateTimeField(default=timezone.now)

    history = HistoryManager('int_field', 'str_field', 'date_field')


class ModelB(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)

    int_field = models.IntegerField()
    history = HistoryManager(int_field)
