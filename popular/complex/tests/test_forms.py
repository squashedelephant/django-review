# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from bs4 import BeautifulSoup
from random import randint, random

from django.contrib.auth.models import User
from django.test import TestCase

from complex.forms import EventForm, SensorForm
from complex.models import Event, Sensor
from complex.tests.utils import get_alt_units, get_pressure_units
from complex.tests.utils import get_random_name, get_random_sku, get_serial_no
from complex.tests.utils import get_temp_units, get_ws_units

class TestSensorForm(TestCase):
    fixtures = ['sensor', 'user']

    def setUp(self):
        self.user = User.objects.get(username='qa')
        value = randint(1000, 5000)
        self.data_valid = {'name': get_random_name(),
                           'sku': get_random_sku(),
                           'serial_no': get_serial_no(),
                           'temp_units': get_temp_units(),
                           'pressure_units': get_pressure_units(),
                           'alt_units': get_alt_units(),
                           'ws_units': get_ws_units()}
        self.data_long = self.data_valid.copy()
        self.data_long.update({'name': 'Exceedingly Long {}'.format(value)})
        self.data_empty = self.data_valid.copy()
        self.data_empty.update({'name': None})
        self.data_blank = self.data_valid.copy()
        self.data_blank.update({'name': ''})

    def tearDown(self):
        self.data_valid = None
        self.data_long = None
        self.data_empty = None
        self.data_blank = None

    def test_01_name_valid(self):
        form = SensorForm(data=self.data_valid)
        soup = BeautifulSoup(str(form), 'html.parser')
        for option in soup.find(attrs={'name': 'created_by'}).findAll('option'):
            if option.text == self.user.username:
                self.data_valid.update({'created_by': option['value']})
        form = SensorForm(data=self.data_valid)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.is_bound)
        self.assertEqual(self.data_valid['name'],
                         form.data['name'])

    def test_02_name_too_long(self):
        #{'temp_units': [u'This field is required.'], 'alt_units': [u'This field is required.'], 'ws_units': [u'This field is required.'], 'created_by': [u'This field is required.'], 'pressure_units': [u'This field is required.']}
        form = SensorForm(data=self.data_long)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.is_bound)
        self.assertEqual(1, len(form.errors['name']))
        errmsg = u'Ensure this value has at most 20 characters (it has 21).'
        self.assertEqual(errmsg,
                         form.errors['name'][0])

    def test_03_name_empty(self):
        form = SensorForm(data=self.data_empty)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.is_bound)
        self.assertEqual(1, len(form.errors['name']))
        self.assertEqual(u'This field is required.',
                         form.errors['name'][0])


    def test_04_name_blank(self):
        form = SensorForm(data=self.data_blank)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.is_bound)
        self.assertEqual(1, len(form.errors['name']))
        self.assertEqual(u'This field is required.',
                         form.errors['name'][0])

    def ttest_05_object(self):
        form = SensorForm(data=self.data_valid)
        self.assertIn('name', str(form))
        self.assertEqual('<SensorForm bound=True, valid=True, fields=(name;serial_no)>',
                         repr(form))
