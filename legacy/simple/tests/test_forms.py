# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal
from random import randint, random

from django.contrib.auth.models import User
from django.test import TestCase

from simple.forms import WidgetForm

class TestSimpleForm(TestCase):
    def setUp(self):
        value = randint(1000, 5000)
        cost = Decimal('%0.2f' % (value * 1.00 * random()))
        self.data_valid = {'name': 'Moon',
                           'cost': cost}
        self.data_long = {'name': 'Exceedingly Long {}'.format(value),
                          'cost': cost}
        self.data_empty = {'name': None,
                           'cost': value * 1.00 * random()}
        self.data_blank = {'name': '',
                           'cost': cost}

    def tearDown(self):
        self.data = None

    def ttest_01_name_valid(self):
        form = WidgetForm(data=self.data_valid)
        print(form.errors)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.is_bound)
        self.assertEqual(self.data_valid['name'], form.data['name'])

    def ttest_02_name_too_long(self):
        form = WidgetForm(data=self.data_long)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.is_bound)
        self.assertEqual(1, len(form.errors['name']))
        self.assertEqual(u'Ensure this value has at most 20 characters (it has 21).',
                         form.errors['name'][0])

    def ttest_03_name_empty(self):
        form = WidgetForm(data=self.data_empty)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.is_bound)
        self.assertEqual(1, len(form.errors['name']))
        self.assertEqual(u'This field is required.',
                         form.errors['name'][0])

    def ttest_04_name_blank(self):
        form = WidgetForm(data=self.data_blank)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.is_bound)
        self.assertEqual(1, len(form.errors['name']))
        self.assertEqual(u'This field is required.',
                         form.errors['name'][0])

    def ttest_05_object(self):
        form = WidgetForm(data=self.data_valid)
        self.assertIn('name', str(form).split())
        self.assertEqual("<class 'simple.forms.WidgetForm'>.'name_cost'", repr(form))

