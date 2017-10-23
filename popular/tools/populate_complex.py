#!/usr/bin/env python

from decimal import Decimal
from os import environ
from random import randint, random
from sys import argv, exit, path

from django import setup
from django.db import IntegrityError

def assign_user_permissions():
    from django.contrib.auth.models import User
    from tools.users_and_groups import get_users, get_event_permissions
    from tools.users_and_groups import get_sensor_permissions
    users = get_users()
    event_perms = get_event_permissions()
    sensor_perms = get_sensor_permissions()
    read_only_users = ['view']
    write_only_users = ['add']
    readwrite_users= ['change']
    delete_users = ['delete']
    full_access_users = ['qa']
    for u in users:
        try:
            user = User.objects.get(username=users[u]['username'])
            if u in read_only_users:
                pass
            if u in write_only_users:
                user.user_permissions.add(sensor_perms['add_sensor'])
                user.user_permissions.add(event_perms['add_event'])
            if u in readwrite_users:
                # hack because test must create before update
                user.user_permissions.add(sensor_perms['add_sensor'])
                user.user_permissions.add(event_perms['add_event'])
                user.user_permissions.add(sensor_perms['change_sensor'])
                user.user_permissions.add(event_perms['change_event'])
            if u in delete_users:
                # hack because test must create before delete
                user.user_permissions.add(sensor_perms['add_sensor'])
                user.user_permissions.add(event_perms['add_event'])
                user.user_permissions.add(sensor_perms['delete_sensor'])
                user.user_permissions.add(event_perms['delete_event'])
            if u in full_access_users:
                user.user_permissions.add(sensor_perms['full_access'])
                user.user_permissions.add(event_perms['full_access'])
        except Exception as e:
            print('ERROR: failed in assign_user_permissions')
            exit('ERROR: {}'.format(str(e)))
    return

def assign_group_permissions():
    from django.contrib.auth.models import Group, User
    from tools.users_and_groups import get_groups, get_event_permissions
    from tools.users_and_groups import get_sensor_permissions
    sensor_perms = get_sensor_permissions()
    event_perms = get_event_permissions()
    search_users = ['view']
    write_only_users = ['add']
    readwrite_users= ['change']
    delete_users = ['delete']
    full_access_users = ['qa']
    for g in get_groups():
        try:
            group = Group.objects.get(name=g)
            if g == 'view':
                for u in search_users:
                    user = User.objects.get(username=u)
                    user.groups.add(group)
                    group.user_set.add(user)
            elif g == 'add':
                group.permissions.add(sensor_perms['add_sensor'])
                group.permissions.add(event_perms['add_event'])
                for u in write_only_users:
                    user = User.objects.get(username=u)
                    user.groups.add(group)
                    group.user_set.add(user)
            elif g == 'change':
                group.permissions.add(sensor_perms['change_sensor'])
                group.permissions.add(event_perms['change_event'])
                for u in readwrite_users:
                    user = User.objects.get(username=u)
                    user.groups.add(group)
                    group.user_set.add(user)
            elif g == 'delete':
                group.permissions.add(sensor_perms['delete_sensor'])
                group.permissions.add(event_perms['delete_event'])
                for u in delete_users:
                    user = User.objects.get(username=u)
                    user.groups.add(group)
                    group.user_set.add(user)
            elif g == 'full_access':
                group.permissions.add(sensor_perms['full_access'])
                group.permissions.add(event_perms['full_access'])
                for u in full_access_users:
                    user = User.objects.get(username=u)
                    user.groups.add(group)
                    group.user_set.add(user)
        except Exception as e:
            print('ERROR: failed in assign_group_permissions')
            exit('ERROR: {}'.format(str(e)))
    return

def populate_sensors():
    from django.contrib.auth.models import User
    from simple.models import Sensor
    from simple.tests.utils import xxx
    try:
        user = User.objects.get(username='qa')
    except User.DoesNotExist as e:
        exit('ERROR: create missing username: qa')
    if hasattr(user, 'id'):
        sensors = []
        for sku in get_skus():
            while True:
                ref = randint(1, 100)
                kwargs = {'name': 'Sensor {}'.format(ref),
                          'sku': sku,
                          'created_by': user,
                          'deleted': False}
                try:
                    s = Store.objects.create(**kwargs)
                    stores.append(s)
                    break
                except IntegrityError as e:
                    if str(e).endswith('name'):
                        s = Store.objects.filter(name=kwargs['name'])
                    elif str(e).endswith('location'):
                        s = Store.objects.filter(location=kwargs['location'])
                    stores.append(s[0])
                    break
        return sensors
    else:
        error = 'script assumes User: qa exists as first user created!'
        exit('ERROR: {}'.format(error))

def populate_events(sensors, n):
    from django.contrib.auth.models import User
    from simple.models import Event, Sensor
    try:
        user = User.objects.get(username='qa')
    except User.DoesNotExist as e:
        exit('ERROR: create missing username: qa')
    if hasattr(user, 'id'):
        events = []
        for i in range(n):
            while True:
                idx_s = randint(0, len(sensors) - 1)
                quantity = randint(1, 100)
                kwargs = {'store': stores[idx_s],
                          'widget': widgets[idx_w],
                          'quantity': quantity,
                          'created_by': user,
                          'deleted': False}
                try:
                    e = Event.objects.create(**kwargs)
                    events.append(i)
                    break
                except IntegrityError:
                    e = Event.objects.filter(sensor=kwargs['sensor'],
                                             widget=kwargs['widget'])
                    events.append(e[0])
                    continue
    else:
        error = 'script assumes User: qa exists as first user created!'
        exit('ERROR: {}'.format(error))

def main():
    path.append('/Users/tim/Documents/workspace/python/django-review/popular/')
    environ.setdefault("DJANGO_SETTINGS_MODULE", "popular.settings")
    setup()
    max = 10
    assign_user_permissions()
    assign_group_permissions()
    sensors = populate_sensors()
    populate_events(sensors, max)
    return

if __name__ == '__main__':
    main()
    exit(0)
