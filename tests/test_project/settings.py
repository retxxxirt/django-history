SECRET_KEY = '+GG0EtOp7fIveaPPYFbXdToj6OYBkKKNznMyaxtjHEFEfUd9Eo'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}

INSTALLED_APPS = [
    'django_history',
    'test_app'
]
