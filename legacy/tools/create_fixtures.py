from os import environ
from sys import exit, path

from django import setup
from django.conf import settings
from django.core.management import execute_from_command_line

def get_db_tables():
    db_tables = {'user.json': 'auth.user',
                 'group.json': 'auth.group',
                 'permission.json': 'auth.permission',
                 'group_permission.json': 'auth.group_permissions',
                 'user_groups.json': 'auth.user_groups',
                 'user_permission.json': 'auth.user_user_permissions',
                 'inventory.json': 'simple.inventory'}
                 'store.json': 'simple.store'}
                 'widget.json': 'simple.widget'}
    return db_tables

def main():
    path.append('/Users/tim/Documents/workspace/python/django-review/legacy/')
    environ.setdefault("DJANGO_SETTINGS_MODULE", "legacy.settings")
    setup()
    for key, value in get_db_tables().items():
        print('key: {}'.format(key))
        print('value: {}'.format(value))
        execute_from_command_line(['manage.py',
                                   'dumpdata',
                                   '--indent',
                                   '4',
                                   '--output',
                                   '{}/{}'.format(settings.FIXTURE_DIRS[0], key),
                                   value])
    return

if __name__ == '__main__':
    main()
    exit(0)
