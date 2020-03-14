from django.apps import AppConfig, apps
from django.db.models.signals import pre_save, post_save

from .register import registered_models
from .signals import pre_save_handler, post_save_handler


class DjangoHistoryConfig(AppConfig):
    name = 'django_history'

    def ready(self):
        pre_save.connect(pre_save_handler)
        post_save.connect(post_save_handler)

        for model in apps.get_models():
            registered_models[model._meta.db_table] = model
