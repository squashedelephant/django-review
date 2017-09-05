from random import randint

def _format_name(n):
    f = []
    for c in n:
        if c in ['-', ' ']:
            f.append('_')
        else:
            f.append(c)
    return ''.join(f)

def _get_suffix():
    return randint(10000, 50000)

def flatten_list_of_tuples(l):
    s = set()
    for e in l:
        for v in e:
            if isinstance(v, (str, int, float)):
                s.add(v)
            else:
                s.add(str(v))
    return list(s)

def get_name(n):
    name = '{} {}'.format(' '.join(n.split()[0:-1]), _get_suffix())
    return name

def get_contact(c):
    contact = '{} {}'.format(' '.join(c.split()[0:-1]), _get_suffix())
    return contact

def get_phone():
    country = randint(1, 160)
    region = randint(1, 999)
    area = randint(1, 999)
    home = randint(1, 9999)
    return '{}-{}-{}-{}'.format(country, region, area, home)

def get_email(c):
    return '{}@{}.random.org'.format(_format_name(c), _get_suffix())

def get_bad_email(c):
    return '{}@invalid.org'.format(_format_name(c))
