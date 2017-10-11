#!/usr/bin/env python

from decimal import Decimal
from os import environ
from random import randint, random
from sys import argv, exit, path

from django import setup
from django.db import IntegrityError

def assign_user_permissions():
    from django.contrib.auth.models import User
    from tools.users_and_groups import get_users, get_inventory_permissions
    from tools.users_and_groups import get_store_permissions
    from tools.users_and_groups import get_widget_permissions
    users = get_users()
    inv_perms = get_inventory_permissions()
    store_perms = get_store_permissions()
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
                #user.user_permissions.add(inv_perms['add_inventory'])
                user.user_permissions.add(store_perms['add_store'])
                user.user_permissions.add(widget_perms['add_widget'])
            if u in readwrite_users:
                # hack because test must create before update
                #user.user_permissions.add(inv_perms['add_inventory'])
                user.user_permissions.add(store_perms['add_store'])
                user.user_permissions.add(widget_perms['add_widget'])
                #user.user_permissions.add(inv_perms['change_inventory'])
                user.user_permissions.add(store_perms['change_store'])
                user.user_permissions.add(widget_perms['change_widget'])
            if u in delete_users:
                # hack because test must create before delete
                #user.user_permissions.add(inv_perms['add_inventory'])
                user.user_permissions.add(store_perms['add_store'])
                user.user_permissions.add(widget_perms['add_widget'])
                #user.user_permissions.add(inv_perms['delete_inventory'])
                user.user_permissions.add(store_perms['delete_store'])
                user.user_permissions.add(widget_perms['delete_widget'])
            if u in full_access_users:
                #user.user_permissions.add(inv_perms['full_access'])
                user.user_permissions.add(store_perms['full_access'])
                user.user_permissions.add(widget_perms['full_access'])
        except Exception as e:
            print('ERROR: failed in assign_user_permissions')
            exit('ERROR: {}'.format(str(e)))
    return

def assign_group_permissions():
    from django.contrib.auth.models import Group, User
    from tools.users_and_groups import get_groups, get_widget_permissions
    from tools.users_and_groups import get_store_permissions
    from tools.users_and_groups import get_widget_permissions
    #inv_perms = get_inventory_permissions()
    store_perms = get_store_permissions()
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
                #group.permissions.add(inv_perms['add_inventory'])
                group.permissions.add(store_perms['add_store'])
                group.permissions.add(widget_perms['add_widget'])
                for u in write_only_users:
                    user = User.objects.get(username=u)
                    user.groups.add(group)
                    group.user_set.add(user)
            elif g == 'change':
                #group.permissions.add(inv_perms['change_inventory'])
                group.permissions.add(store_perms['change_store'])
                group.permissions.add(widget_perms['change_widget'])
                for u in readwrite_users:
                    user = User.objects.get(username=u)
                    user.groups.add(group)
                    group.user_set.add(user)
            elif g == 'delete':
                #group.permissions.add(inv_perms['delete_inventory'])
                group.permissions.add(store_perms['delete_store'])
                group.permissions.add(widget_perms['delete_widget'])
                for u in delete_users:
                    user = User.objects.get(username=u)
                    user.groups.add(group)
                    group.user_set.add(user)
            elif g == 'full_access':
                #group.permissions.add(inv_perms['full_access'])
                group.permissions.add(store_perms['full_access'])
                group.permissions.add(widget_perms['full_access'])
                for u in full_access_users:
                    user = User.objects.get(username=u)
                    user.groups.add(group)
                    group.user_set.add(user)
        except Exception as e:
            print('ERROR: failed in assign_group_permissions')
            exit('ERROR: {}'.format(str(e)))
    return

def populate_stores():
    from django.contrib.auth.models import User
    from simple.models import Store
    from simple.tests.utils import get_locations
    try:
        user = User.objects.get(username='qa')
    except User.DoesNotExist as e:
        exit('ERROR: create missing username: qa')
    if hasattr(user, 'id'):
        stores = []
        locations = get_locations()
        for location in locations:
            while True:
                ref = randint(1, 100)
                kwargs = {'name': 'Store {}'.format(ref),
                          'location': location,
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
        return stores
    else:
        error = 'script assumes User: qa exists as first user created!'
        exit('ERROR: {}'.format(error))

def populate_widgets(n):
    from django.contrib.auth.models import User
    from simple.models import Widget
    from simple.tests.utils import get_random_cost, get_random_sku
    try:
        user = User.objects.get(username='qa')
    except User.DoesNotExist as e:
        exit('ERROR: create missing username: qa')
    if hasattr(user, 'id'):
        widgets = []
        for i in range(n):
            while True:
                ref = randint(10000, 50000)
                kwargs = {'name': 'Random Widget {}'.format(ref),
                          'sku': get_random_sku(),
                          'cost': get_random_cost(),
                          'created_by': user,
                          'deleted': False}
                try:
                    w = Widget.objects.create(**kwargs)
                    widgets.append(w)
                    break
                except IntegrityError as e:
                    if str(e).endswith('name'):
                        w = Widget.objects.filter(name=kwargs['name'])
                    elif str(e).endswith('sku'):
                        w = Widget.objects.filter(sku=kwargs['sku'])
                    widgets.append(w[0])
                    break
        return widgets
    else:
        error = 'script assumes User: qa exists as first user created!'
        exit('ERROR: {}'.format(error))

def populate_inventory(stores, widgets, n):
    from django.contrib.auth.models import User
    from simple.models import Inventory, Store, Widget
    try:
        user = User.objects.get(username='qa')
    except User.DoesNotExist as e:
        exit('ERROR: create missing username: qa')
    if hasattr(user, 'id'):
        inventory = []
        for i in range(n):
            while True:
                idx_s = randint(0, len(stores) - 1)
                idx_w = randint(0, len(widgets) - 1)
                quantity = randint(1, 100)
                kwargs = {'store': stores[idx_s],
                          'widget': widgets[idx_w],
                          'quantity': quantity,
                          'created_by': user,
                          'deleted': False}
                try:
                    i = Inventory.objects.create(**kwargs)
                    inventory.append(i)
                    break
                except IntegrityError:
                    i = Inventory.objects.filter(store=kwargs['store'],
                                                 widget=kwargs['widget'])
                    inventory.append(i[0])
                    continue
    else:
        error = 'script assumes User: qa exists as first user created!'
        exit('ERROR: {}'.format(error))

def main():
    path.append('/Users/tim/Documents/workspace/python/django-review/legacy/')
    environ.setdefault("DJANGO_SETTINGS_MODULE", "legacy.settings")
    setup()
    max = 10
    assign_user_permissions()
    assign_group_permissions()
    stores = populate_stores()
    widgets = populate_widgets(max)
    populate_inventory(stores, widgets, max)
    return

if __name__ == '__main__':
    main()
    exit(0)
