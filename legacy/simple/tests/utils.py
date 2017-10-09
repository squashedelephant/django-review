from decimal import Decimal
from random import randint, random

def get_random_sku():
    ref1 = randint(100, 999)
    ref2 = randint(100, 999)
    ref3 = randint(10, 99)
    return '{0}-{1}-{2}'.format(ref1, ref2, ref3)

def get_random_cost():
    ref_i = randint(1, 1000)
    ref_f = random() * 1.00 + 1
    return float(Decimal('%0.2f' % (ref_i * ref_f)))

def get_locations():
    locations = ['Albany', 'Berkeley', 'El Cerrito', 'Emeryville',
                 'Hercules', 'Pinole', 'Rodeo', 'San Pablo']
    return locations
