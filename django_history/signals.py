from django.db.models import Model


def pre_save_handler(instance: Model, **kwargs):
    from django_history.register import registered_managers

    if instance.__class__ in registered_managers:
        registered_managers[instance.__class__].pre_save(instance)


def post_save_handler(instance: Model, **kwargs):
    from django_history.register import registered_managers

    if instance.__class__ in registered_managers:
        registered_managers[instance.__class__].post_save(instance)
