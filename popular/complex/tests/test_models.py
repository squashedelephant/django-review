# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.management import call_command
from django.db import IntegrityError
from django.test import TestCase

from complex.models import Event, Sensor
from complex.tests.utils import get_alt_units, get_pressure_units
from complex.tests.utils import get_random_name, get_random_sku, get_serial_no
from complex.tests.utils import get_temp_units, get_ws_units

class TestSensorModel(TestCase):
    fixtures = ['sensor', 'user']

    def setUp(self):
        user = User.objects.get(username='qa')
        self.data= {'created_by': user,
                    'name': get_random_name(),
                    'sku': get_random_sku(),
                    'serial_no': get_serial_no(),
                    'temp_units': get_temp_units(),
                    'pressure_units': get_pressure_units(),
                    'alt_units': get_alt_units(),
                    'ws_units': get_ws_units()}

    def tearDown(self):
        self.data = None

    def test_01_object(self):
        s = Sensor()
        self.assertEqual("<class 'complex.models.Sensor'>", repr(s))
        s = Sensor.objects.create(**self.data)
        self.assertEqual('{0}:{1}'.format(self.data['name'],
                                          self.data['serial_no']),
                         str(s))
        self.assertEqual("<class 'complex.models.Sensor'>:{}".format(s.id),
                                                                     repr(s))

    def test_02_create(self):
        s = Sensor.objects.create(**self.data)
        self.assertLessEqual(1, s.id)

    def test_03_get(self):
        expected = Sensor.objects.create(**self.data)
        actual = Sensor.objects.get(id=expected.id)
        self.assertEqual(expected.id, actual.id)

    def test_04_update(self):
        expected = Sensor.objects.create(**self.data)
        name = get_random_name()
        expected.name = name
        sku = get_random_sku()
        expected.sku = sku
        expected.save()
        actual = Sensor.objects.get(id=expected.id)
        self.assertEqual(name, actual.name)
        self.assertEqual(sku, actual.sku)

    def test_05_delete(self):
        expected = Sensor.objects.create(**self.data)
        expected.delete()
        with self.assertRaises(Sensor.DoesNotExist) as context:
            Sensor.objects.get(pk=expected.id)
        msg = 'Sensor matching query does not exist'
        self.assertIn(msg, str(context.exception))

    def test_06_filter(self):
        names = []
        skus = []
        serials = []
        for i in range(10):
            names.append(get_random_name())
            skus.append(get_random_sku())
            serials.append(get_serial_no())
        for idx in range(len(names)):
            self.data.update({'name': names[idx],
                              'sku': skus[idx],
                              'serial_no': serials[idx],
                              'camera': True})
            Sensor.objects.create(**self.data)
        actual = Sensor.objects.filter(camera=True)
        self.assertEqual(len(names), len(actual))

    def test_07_save(self):
        expected = Sensor(**self.data)
        expected.save()
        self.assertIsNone(expected.link)
        self.assertIsNone(expected.dlink)
        self.assertIsNone(expected.ulink)
        actual = Sensor.objects.get(id=expected.id)
        self.assertIsNotNone(actual.link)
        self.assertIsNotNone(actual.dlink)
        self.assertIsNotNone(actual.ulink)

