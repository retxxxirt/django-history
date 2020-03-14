# /ust/bin/env python
import os
import sys

from django.core.management import execute_from_command_line

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
    sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_project.settings')

    execute_from_command_line(sys.argv)
