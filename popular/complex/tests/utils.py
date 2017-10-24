from decimal import Decimal
from random import randint, random

from complex.models import Event, Sensor

from django.conf import settings
from django.utils.timezone import datetime, pytz, timedelta

def get_random_name():
    names = ['Alpha', 'Beta', 'Delta', 'Epsilon', 'Gamma', 'Zeta',
             'Eta', 'Theta', 'Iota', 'Kappa', 'Lambda', 'Mu', 'Nu',
             'Xi', 'Omikron', 'Pi', 'Rho', 'Sigma', 'Tau', 'Upsilon',
             'Phi', 'Chi', 'Psi', 'Omega']
    idx = randint(0, len(names) - 1)
    return names[idx]

def get_random_sku():
    ref1 = randint(100, 999)
    ref2 = randint(100, 999)
    ref3 = randint(10, 99)
    return '{0}-{1}-{2}'.format(ref1, ref2, ref3)

def get_serial_no():
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    digits = '0123456789'
    word_len = randint(8, 15)
    tmp = []
    for i in range(word_len):
        flip = randint(0, 1)
        if flip == 1:
            tmp.append(chars[randint(0, len(chars) - 1)])
        else:
            tmp.append(digits[randint(0, len(digits) - 1)])
    return ''.join(tmp)

def get_temp_units():
    units = Sensor.TEMPERATURE_UNITS
    return units[randint(0, len(units) - 1)][0]

def get_pressure_units():
    units = Sensor.PRESSURE_UNITS
    return units[randint(0, len(units) - 1)][0]

def get_alt_units():
    units = Sensor.ALTITUDE_UNITS
    return units[randint(0, len(units) - 1)][0]

def get_ws_units():
    units = Sensor.WINDSPEED_UNITS
    return units[randint(0, len(units) - 1)][0]

    locations = Event.LOCATIONS
    return locations[randint(0, len(locations) - 1)][0]

def get_random_location():
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
    return float(Decimal('%0.2f' % (randint(-273, 1000) * random() * 1.00)))

def get_avg_pressure():
    return float(Decimal('%0.2f' % (randint(0, 1000) * random() * 1.00)))

def get_pct_humidity():
    return randint(0, 100)

def get_altitude():
    return randint(0, 100000)

def get_windspeed():
    return randint(0, 1000)

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

