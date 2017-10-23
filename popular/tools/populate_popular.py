#!/usr/bin/env python

from os import environ
from random import randint
from sys import argv, exit, path

from django import setup
from django.db.utils import IntegrityError

def load_users():
    from django.contrib.auth.models import User
    from tools.utils import get_users
    users = get_users()
    for user in users:
        try:
            User.objects.create_user(**users[user])
        except IntegrityError:
            pass
        except Exception as e:
            exit('ERROR: {}'.format(str(e)))
    return

def load_groups():
    from django.contrib.auth.models import Group
    from tools.utils import get_groups
    groups = get_groups()
    for group in groups:
        try:
            Group.objects.create(name=group)
        except IntegrityError:
            pass
        except Exception as e:
            exit('ERROR: {}'.format(str(e)))
    return

def main():
    path.append('/Users/tim/Documents/workspace/python/django-review/popular/')
    environ.setdefault("DJANGO_SETTINGS_MODULE", "popular.settings")
    setup()
    max = 10
    load_users()
    load_groups()
    return

if __name__ == '__main__':
    main()
    exit(0)
