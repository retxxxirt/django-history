from typing import Any, Iterator, List, Type

from django.db.models import Field, Model, QuerySet
from django_history.register import registered_managers


class HistoryQuerySet(QuerySet):
    def field(self, field: str) -> QuerySet:
        return self.filter(field_name=field)

    def fields(self, *fields: str) -> QuerySet:
        return self.filter(field_name__in=fields)

    def items(self) -> Iterator[tuple]:
        for history in self.all():
            yield history.added_at, history.field_value


class HistoryMangerDescriptor:
    def __init__(self, manager: 'HistoryManager'):
        self.model_name = manager.model._meta.db_table

    def __get__(self, instance: Model, *args) -> QuerySet:
        from django_history.models import History

        default_filter = {'model_name': self.model_name}

        if instance is not None:
            default_filter['instance_pk'] = instance.pk

        return HistoryQuerySet(History).filter(**default_filter)


class HistoryManager:
    def __init__(self, *fields_or_names: Any):
        self.fields_to_create = []
        self.model, self.fields = None, []
        self.fields_or_names = fields_or_names

    @staticmethod
    def _get_model_fields(model: Type[Model], *fields_or_names: Any) -> List[Field]:
        fields = []

        for field_or_name in fields_or_names:
            if isinstance(field_or_name, str):
                fields.append(model._meta.get_field(field_or_name))
            elif isinstance(field_or_name, Field):
                fields.append(field_or_name)

        return fields

    def contribute_to_class(self, model: Type[Model], name: str):
        self.fields = self._get_model_fields(model, *self.fields_or_names)

        self.model, registered_managers[model] = model, self
        setattr(model, name, HistoryMangerDescriptor(self))

    def pre_save(self, instance: Model):
        try:
            db_instance = self.model.objects.get(pk=instance.pk)
        except self.model.DoesNotExist:
            self.fields_to_create = self.fields
        else:
            self.fields_to_create = []

            for field in instance._meta.fields:
                if field in self.fields and getattr(instance, field.name) != getattr(db_instance, field.name):
                    self.fields_to_create.append(field)

    def post_save(self, instance: Model):
        from django_history.models import History

        instance_pk = instance._meta.get_field(instance._meta.pk.name).value_to_string(instance)

        for field in self.fields_to_create:
            History.objects.create(
                model_name=self.model._meta.db_table, instance_pk=instance_pk,
                field_name=field.name, field_value=field.get_prep_value(getattr(instance, field.name))
            )
