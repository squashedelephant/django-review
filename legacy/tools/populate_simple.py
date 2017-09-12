#!/usr/bin/env python

from os import environ
from random import randint, random
from sys import argv, exit, path

from django import setup
from django.db.utils import IntegrityError

def assign_user_permissions():
    from django.contrib.auth.models import User
    from tools.users_and_groups import get_users, get_widget_permissions
    users = get_users()
    widget_perms = get_widget_permissions()
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
                user.user_permissions.add(widget_perms['add_widget'])
            if u in readwrite_users:
                # hack because test must create before update
                user.user_permissions.add(widget_perms['add_widget'])
                user.user_permissions.add(widget_perms['change_widget'])
            if u in delete_users:
                # hack because test must create before delete
                user.user_permissions.add(widget_perms['add_widget'])
                user.user_permissions.add(widget_perms['delete_widget'])
            if u in full_access_users:
                user.user_permissions.add(widget_perms['full_access'])
        except Exception as e:
            print('ERROR: failed in assign_user_permissions')
            exit('ERROR: {}'.format(str(e)))
    return

def assign_group_permissions():
    from django.contrib.auth.models import Group, User
    from tools.users_and_groups import get_groups, get_widget_permissions
    widget_perms = get_widget_permissions()
    search_users = ['view']
    write_only_users = ['add']
    readwrite_users= ['change']
    delete_users = ['delete']
    full_access_users = ['superuser', 'staff', 'qa']
    for g in get_groups():
        try:
            group = Group.objects.get(name=g)
            if g == 'view':
                for u in search_users:
                    user = User.objects.get(username=u)
                    user.groups.add(group)
                    group.user_set.add(user)
            elif g == 'add':
                group.permissions.add(widget_perms['add_widget'])
                for u in write_only_users:
                    user = User.objects.get(username=u)
                    user.groups.add(group)
                    group.user_set.add(user)
            elif g == 'change':
                group.permissions.add(widget_perms['change_widget'])
                for u in readwrite_users:
                    user = User.objects.get(username=u)
                    user.groups.add(group)
                    group.user_set.add(user)
            elif g == 'delete':
                group.permissions.add(widget_perms['delete_widget'])
                for u in delete_users:
                    user = User.objects.get(username=u)
                    user.groups.add(group)
                    group.user_set.add(user)
            elif g == 'full_access':
                group.permissions.add(widget_perms['full_access'])
                for u in full_access_users:
                    user = User.objects.get(username=u)
                    user.groups.add(group)
                    group.user_set.add(user)
        except Exception as e:
            print('ERROR: failed in assign_group_permissions')
            exit('ERROR: {}'.format(str(e)))
    return

def load_widgets(n):
    from django.contrib.auth.models import User
    from simple.models import Widget
    try:
        user = User.objects.get(username='qa')
    except User.DoesNotExist as e:
        exit('ERROR: create missing username: qa')
    if hasattr(user, 'id'):
        for i in range(n):
            ref = randint(10000, 50000)
            kwargs = {'name': 'Random Widget {}'.format(ref),
                      'cost': ref * 1.00 * random() / 100,
                      'created_by': user,
                      'deleted': False}
            try:
                widget = Widget.objects.create(**kwargs)
            except IntegrityError:
                pass
    else:
        error = 'script assumes User: qa exists as first user created!'
        exit('ERROR: {}'.format(error))

def main():
    path.append('/Users/tim/Project/django-review/legacy/')
    environ.setdefault("DJANGO_SETTINGS_MODULE", "legacy.settings")
    setup()
    max = 10
    assign_user_permissions()
    assign_group_permissions()
    load_widgets(max)
    return

if __name__ == '__main__':
    main()
    exit(0)
