#!/usr/bin/env python

from os import environ
from random import randint
from sys import argv, exit, path

from django import setup


def load_users():
    from django.contrib.auth.models import User
    from tools.users import get_users
    users = get_users()
    for user in users:
        try:
            user = User.objects.create_user(**users[user])
        except Exception as e:
            exit('ERROR: {}'.format(str(e)))
    return

def main():
    path.append('/Users/tim/Project/django-review/legacy/')
    environ.setdefault("DJANGO_SETTINGS_MODULE", "legacy.settings")
    setup()
    max = 10
    load_users()
    return

if __name__ == '__main__':
    main()
    exit(0)
