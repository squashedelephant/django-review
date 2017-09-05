#!/usr/bin/env python

from os import environ
from random import randint
from sys import argv, exit, path

from django import setup


def assign_user_permissions():
    from django.contrib.auth.models import Group, Permission, User
    from django.contrib.contenttypes.models import ContentType
    from simple.models import Widget
    from tools.users import get_users
    content_type = ContentType.objects.get_for_model(Widget)
    Permission.objects.create(codename='widget.full_access',
                                        name='User may Add, View, Change, Delete',
                                        content_type=content_type)
    add_widget = Permission.objects.get(codename='add_widget')
    change_widget = Permission.objects.get(codename='change_widget')
    delete_widget = Permission.objects.get(codename='delete_widget')
    full_access = Permission.objects.get(codename='widget.full_access')
    users = get_users()
    read_only_users = ['view']
    write_only_users = ['add']
    readwrite_users= ['change']
    delete_users = ['delete']
    full_access_users = ['superuser', 'staff', 'qa']
    for u in users:
        try:
            user = User.objects.get(username=users[u]['username'])
            if u in read_only_users:
                pass
            if u in write_only_users:
                user.user_permissions.add(add_widget)
            if u in readwrite_users:
                # hack because test must create before update
                user.user_permissions.add(add_widget)
                user.user_permissions.add(change_widget)
            if u in delete_users:
                # hack because test must create before delete
                user.user_permissions.add(add_widget)
                user.user_permissions.add(delete_widget)
            if u in full_access_users:
                user.user_permissions.add(full_access)
        except Exception as e:
            exit('ERROR: {}'.format(str(e)))
    return

def load_widgets(n):
    from django.contrib.auth.models import User
    from django.core.urlresolvers import reverse
    from simple.models import Widget
    try:
        user = User.objects.get(username='qa')
    except User.DoesNotExist as e:
        exit('ERROR: create missing username: qa')
    if hasattr(user, 'id'):
        for i in range(n):
            ref = randint(10000, 50000)
            country = randint(1, 200)
            area = randint(100, 999)
            prefix = randint(100, 999)
            home = randint(1000, 9999)
            created_by = user
            name = 'Random Widget {}'.format(ref)
            deleted = False 
            kwargs = {'name': name,
                      'created_by': created_by,
                      'deleted': deleted}
            widget = Widget.objects.create(**kwargs)
    else:
        error = 'script assumes User: qa exists as first user created!'
        exit('ERROR: {}'.format(error))

def main():
    path.append('/Users/tim/Project/django-review/legacy/')
    environ.setdefault("DJANGO_SETTINGS_MODULE", "legacy.settings")
    setup()
    max = 10
    assign_user_permissions()
    load_widgets(max)
    return

if __name__ == '__main__':
    main()
    exit(0)
