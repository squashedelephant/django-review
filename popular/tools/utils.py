def get_groups():
    groups = ['add',
              'change',
              'delete',
              'full_access']
    return groups

def get_users():
    users = {'qa': {'username': 'qa',
                    'password': 'br0k3nc0d3',
                    'email': 'qa@random.org',
                    'is_staff': True,
                    'is_superuser': False,
                    'is_active': True},
             'view': {'username': 'view',
                     'password': 'readonly',
                     'email': 'view@random.org',
                     'is_staff': False,
                     'is_superuser': False,
                     'is_active': True},
             'add': {'username': 'add',
                     'password': 'write',
                     'email': 'add@random.org',
                     'is_staff': False,
                     'is_superuser': False,
                     'is_active': True},
             'change': {'username': 'change',
                        'password': 'readwrite',
                        'email': 'change@random.org',
                        'is_staff': False,
                        'is_superuser': False,
                        'is_active': True},
             'delete': {'username': 'delete',
                        'password': 'write',
                        'email': 'delete@random.org',
                        'is_staff': False,
                        'is_superuser': False,
                        'is_active': True}}
    return users

def get_event_permissions():
    from django.contrib.auth.models import Permission
    from django.contrib.contenttypes.models import ContentType
    from simple.models import Event
    content_type = ContentType.objects.get_for_model(Event)
    try:
        full_access = Permission.objects.get(codename='event.full_access')
    except Permission.DoesNotExist:
        full_access = Permission.objects.create(codename='event.full_access',
                                                name='User may Add, View, Change, Delete',
                                                content_type=content_type)
    add_event = Permission.objects.get(codename='add_event')
    change_event = Permission.objects.get(codename='change_event')
    delete_event = Permission.objects.get(codename='delete_event')
    permissions = {'add_event': add_event,
                   'change_event': change_event,
                   'delete_event': delete_event,
                   'full_access': full_access}
    return permissions

def get_sensor_permissions():
    from django.contrib.auth.models import Permission
    from django.contrib.contenttypes.models import ContentType
    from simple.models import Sensor
    content_type = ContentType.objects.get_for_model(Sensor)
    try:
        full_access = Permission.objects.get(codename='sensor.full_access')
    except Permission.DoesNotExist:
        full_access = Permission.objects.create(codename='sensor.full_access',
                                                name='User may Add, View, Change, Delete',
                                                content_type=content_type)
    add_sensor = Permission.objects.get(codename='add_sensor')
    change_sensor = Permission.objects.get(codename='change_sensor')
    delete_sensor = Permission.objects.get(codename='delete_sensor')
    permissions = {'add_sensor': add_sensor,
                   'change_sensor': change_sensor,
                   'delete_sensor': delete_sensor,
                   'full_access': full_access}
    return permissions
