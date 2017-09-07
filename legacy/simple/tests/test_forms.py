# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from random import randint, random

from django.contrib.auth.models import User
from django.test import TestCase

from simple.forms import WidgetForm

class TestSimpleForm(TestCase):
    def setUp(self):
        value = randint(10000, 50000)
        self.data_valid = {'name': 'Moon',
                           'cost': value * 1.00 * random()}
        self.data_long = {'name': 'Exceedingly Long {}'.format(value),
                          'cost': value * 1.00 * random()}
        self.data_empty = {'name': None,
                          'cost': value * 1.00 * random()}
        self.data_blank = {'name': '',
                          'cost': value * 1.00 * random()}

    def tearDown(self):
        self.data = None

    def test_01_name_valid(self):
        form = WidgetForm(data=self.data_valid)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.is_bound)
        self.assertEqual(self.data_valid['name'], form.data['name'])

    def test_02_name_too_long(self):
        form = WidgetForm(data=self.data_long)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.is_bound)
        self.assertEqual(1, len(form.errors['name']))
        self.assertEqual(u'Ensure this value has at most 20 characters (it has 22).',
                         form.errors['name'][0])

    def test_03_name_empty(self):
        form = WidgetForm(data=self.data_empty)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.is_bound)
        self.assertEqual(1, len(form.errors['name']))
        self.assertEqual(u'This field is required.',
                         form.errors['name'][0])

    def test_04_name_blank(self):
        form = WidgetForm(data=self.data_blank)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.is_bound)
        self.assertEqual(1, len(form.errors['name']))
        self.assertEqual(u'This field is required.',
                         form.errors['name'][0])

    def test_05_object(self):
        form = WidgetForm(data=self.data_valid)
        self.assertIn('name', str(form).split())
        self.assertEqual("<class 'simple.forms.WidgetForm'>.'name_cost'", repr(form))

