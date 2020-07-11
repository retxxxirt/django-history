from distutils.core import setup

setup(
    name='django-history-manager',
    packages=['django_history'],
    package_data={'django_history': ['migrations/*.py']},
    version='0.1.1',
    license='MIT',
    description='History manger for django models.',
    # long_description=open('README.md').read(),
    # long_description_content_type='text/markdown',
    author='retxxxirt',
    author_email='retxxirt@gmail.com',
    url='https://github.com/retxxxirt/django-history',
    keywords=['django history', 'django', 'django history manager', 'django history model', 'django history field'],
    tests_require=(tests_require := ['django==3.0.4']),
    extras_require={'test': tests_require}
)
