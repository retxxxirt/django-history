from datetime import datetime
from uuid import UUID

from django.test import TestCase

from test_app.models import ModelA, ModelB


class ModelATestCase(TestCase):
    def test_create_update(self):
        ModelA(int_field=0, str_field='').save()
        self.assertEqual(ModelA.history.count(), 3)

        ModelA.objects.update_or_create(dict(int_field=1, str_field=' '))
        self.assertEqual(ModelA.history.count(), 5)

        ModelA.objects.update_or_create(dict(int_field=1, str_field=' '))
        self.assertEqual(ModelA.history.count(), 5)

        ModelA.objects.update_or_create(dict(int_field=0, str_field=''))
        self.assertEqual(ModelA.history.count(), 7)

    def test_value_type(self):
        ModelA(int_field=0, str_field='').save()

        for field, type in [('int_field', int), ('str_field', str), ('date_field', datetime)]:
            self.assertIsInstance(ModelA.history.field(field).first().field_value, type)

    def test_field_filter(self):
        (model := ModelA(int_field=0, str_field='')).save()
        self.assertEqual(model.history.field('int_field').count(), 1)

        ModelA.objects.update_or_create(dict(int_field=1))
        self.assertEqual(model.history.field('int_field').count(), 2)

    def test_fields_filter(self):
        (model := ModelA(int_field=0, str_field='')).save()
        self.assertEqual(model.history.fields('int_field', 'str_field').count(), 2)

        ModelA.objects.update_or_create(dict(int_field=1, str_field=' '))
        self.assertEqual(model.history.fields('int_field', 'str_field').count(), 4)

    def test_items_accessor(self):
        (model := ModelA(int_field=0, str_field='')).save()
        ModelA.objects.update_or_create(dict(int_field=1))
        ModelA.objects.update_or_create(dict(int_field=0))

        for index, item in enumerate(model.history.field('int_field').items()):
            self.assertEqual(item[1], index % 2)


class ModelBTestCase(TestCase):
    def test_custom_pk(self):
        (model := ModelB(int_field=0)).save()
        history = model.history.first()

        self.assertIsInstance(history.instance_pk, UUID)
