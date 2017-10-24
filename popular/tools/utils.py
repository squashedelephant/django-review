from decimal import Decimal
from random import randint, random

from django.conf import settings
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import datetime, pytz, timedelta

from complex.models import Event, Sensor

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
             'superuser': {'username': 'superuser',
                           'password': 'fullaccess',
                           'email': 'superuser@random.org',
                           'is_staff': True,
                           'is_superuser': True,
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

def get_sensor_name():
    _ref = randint(1000, 5000)
    return 'Random Sensor {}'.format(_ref)

def get_sku():
    p_ref = randint(100, 999)
    m_ref = randint(10000, 99999)
    e_ref = randint(100, 999)
    return '{}-{}-{}'.format(p_ref, m_ref, e_ref)

def get_serial_no():
    alphabet = 'ABCDEFGHIUJKLMNOPQRSTUVWXYZ'
    numbers = '1234567890'
    sn = []
    for i in range(10):
        letter = alphabet[randint(0, len(alphabet) - 1)]
        digit = numbers[randint(0, len(numbers) - 1)]
        guess = randint(0, 1)
        if guess == 0:
            sn.append(letter)
        else:
            sn.append(digit)
    return ''.join(sn)

def get_timestamp():
    """
    tz: pytz.timezone
    return: datetime.datetime localized to tz
    """
    t = datetime.now()
    #return t.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    return datetime(t.year,
                    t.month,
                    t.day,
                    t.hour,
                    t.minute,
                    t.second,
                    t.microsecond,
                    tzinfo=pytz.timezone(settings.TIME_ZONE))

def get_location():
    locations = Event.LOCATIONS
    l_idx = randint(0, len(locations) - 1)
    return locations[l_idx][0] 

def get_camera():
    camera = Event.CAMERA
    c_idx = randint(0, len(camera) - 1)
    return camera[c_idx][0] 

def get_status():
    status = Event.STATUS
    s_idx = randint(0, len(status) - 1)
    return status[s_idx][0]

def get_avg_temp():
    return float(Decimal(randint(-273, 1000) * random() * 1.00))

def get_avg_pressure():
    return float(Decimal(randint(0, 1000) * random() * 1.00))

def get_pct_humidity():
    return randint(0, 100)

def get_altitude():
    return randint(0, 100000)

def get_windspeed():
    return randint(0, 1000)
