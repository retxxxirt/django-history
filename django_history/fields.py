from typing import TYPE_CHECKING, Any

from django.db.models import TextField

from django_history.register import registered_models

if TYPE_CHECKING:
    from django_history.models import History


class RemoteFieldDescriptor:
    def __init__(self, field: 'RemoteField'):
        self.field = field

    def __get__(self, instance: 'History', *args):
        if instance is None:
            return self.field

        if instance.__dict__[self.field.name] != 'None':
            model = registered_models[instance.model_name]

            if self.field.name == 'instance_pk':
                field = model._meta.get_field(model._meta.pk.name)
            else:
                field = model._meta.get_field(instance.field_name)

            return field.get_prep_value(instance.__dict__[self.field.name])
        return None

    def __set__(self, instance: 'History', value: Any):
        instance.__dict__[self.field.name] = value


class RemoteField(TextField):
    descriptor_class = RemoteFieldDescriptor
