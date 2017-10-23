from decimal import Decimal
from random import randint, random

from complex.models import Sensor

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

