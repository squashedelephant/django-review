#!/usr/bin/env python

from decimal import Decimal
from os import environ
from random import randint
from sys import argv, exit, path

from django import setup
from django.db import IntegrityError

def assign_user_permissions():
    from django.contrib.auth.models import User
    from tools.utils import get_users, get_event_permissions
    from tools.utils import get_sensor_permissions
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
    from tools.utils import get_groups, get_event_permissions
    from tools.utils import get_sensor_permissions
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
    from complex.models import Event, Sensor
    from tools.utils import get_sensor_name, get_sku
    from tools.utils import get_serial_no
    try:
        user = User.objects.get(username='qa')
    except User.DoesNotExist as e:
        exit('ERROR: create missing username: qa')
    if hasattr(user, 'id'):
        sensors = []
        for location in Event.LOCATIONS:
            while True:
                kwargs = {'created_by': user,
                          'name': get_sensor_name(),
                          'sku': get_sku(),
                          'serial_no': get_serial_no(),
                          'climate': True}
                if location in [Event.COCKPIT, Event.FORE_DOOR, Event.AFT_DOOR]:
                    kwargs.update({'camera': True})
                else:
                    kwargs.update({'camera': False})
                try:
                    s = Sensor.objects.create(**kwargs)
                    sensors.append(s)
                    break
                except IntegrityError as e:
                    if str(e).endswith('serial_no'):
                        s = Sensor.objects.filter(serial_no=kwargs['serial_no'])
                    sensors.append(s[0])
                    break
        return sensors
    else:
        error = 'script assumes User: qa exists as first user created!'
        exit('ERROR: {}'.format(error))

def populate_events(sensors, max):
    from django.contrib.auth.models import User
    from complex.models import Event, Sensor
    from tools.utils import get_timestamp, get_location, get_status
    from tools.utils import get_camera, get_avg_temp, get_avg_pressure
    from tools.utils import get_pct_humidity, get_altitude, get_windspeed
    try:
        user = User.objects.get(username='qa')
    except User.DoesNotExist as e:
        exit('ERROR: create missing username: qa')
    if hasattr(user, 'id'):
        for i in range(max):
            idx_s = randint(0, len(sensors) - 1)
            kwargs = {'sensor': sensors[idx_s],
                      'timestamp': get_timestamp(),
                      'location': get_location(),
                      'status': get_status(),
                      'avg_temp': get_avg_temp(),
                      'avg_pressure': get_avg_pressure(),
                      'pct_humidity': get_pct_humidity(),
                      'altitude': get_altitude(),
                      'windspeed': get_windspeed()}
            if sensors[idx_s].camera:
                kwargs.update({'camera': get_camera()})
            e = Event.objects.create(**kwargs)
    else:
        error = 'script assumes User: qa exists as first user created!'
        exit('ERROR: {}'.format(error))

def main():
    path.append('/Users/tim/Documents/workspace/python/django-review/popular/')
    environ.setdefault("DJANGO_SETTINGS_MODULE", "popular.settings")
    setup()
    max = 50
    assign_user_permissions()
    assign_group_permissions()
    sensors = populate_sensors()
    populate_events(sensors, max)
    return

if __name__ == '__main__':
    main()
    exit(0)
