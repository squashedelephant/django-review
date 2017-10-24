# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase

from complex.models import Event, Sensor
from complex.tests.utils import get_alt_units, get_pressure_units
from complex.tests.utils import get_random_name, get_random_sku, get_serial_no
from complex.tests.utils import get_temp_units, get_ws_units
from complex.tests.utils import get_altitude, get_avg_pressure, get_avg_temp
from complex.tests.utils import get_camera, get_pct_humidity, get_random_location
from complex.tests.utils import get_status, get_timestamp, get_windspeed

class TestEventModel(TestCase):
    fixtures = ['event', 'sensor', 'user']

    def setUp(self):
        user = User.objects.get(username='qa')
        self.sensor_data= {'created_by': user,
                           'name': get_random_name(),
                           'sku': get_random_sku(),
                           'serial_no': get_serial_no(),
                           'temp_units': get_temp_units(),
                           'pressure_units': get_pressure_units(),
                           'alt_units': get_alt_units(),
                           'ws_units': get_ws_units()}
        self.event_data = {'timestamp': get_timestamp(),
                           'location': get_random_location(),
                           'status': get_status(),
                           'camera': get_camera(),
                           'avg_temp': get_avg_temp(), 
                           'avg_pressure': get_avg_pressure(), 
                           'pct_humidity': get_pct_humidity(), 
                           'altitude': get_altitude(), 
                           'windspeed': get_windspeed()}

    def tearDown(self):
        self.sensor_data = None
        self.event_data = None

    def test_01_object(self):
        e = Event()
        self.assertEqual("<class 'complex.models.Event'>", repr(e))
        s = Sensor.objects.create(**self.sensor_data)
        self.event_data.update({'sensor': s})
        e = Event.objects.create(**self.event_data)
        self.assertEqual('{0}:{1}'.format(self.event_data['sensor'],
                                          51),
                         str(e))
        self.assertEqual("<class 'complex.models.Event'>:{}".format(e.id),
                                                                    repr(e))

    def test_02_create(self):
        s = Sensor.objects.create(**self.sensor_data)
        self.event_data.update({'sensor': s})
        e = Event.objects.create(**self.event_data)
        self.assertLessEqual(1, e.id)

    def test_03_get(self):
        s = Sensor.objects.create(**self.sensor_data)
        self.event_data.update({'sensor': s}) 
        expected = Event.objects.create(**self.event_data)
        actual = Event.objects.get(id=expected.id)
        self.assertEqual(expected.id, actual.id)

    def test_04_update(self):
        s = Sensor.objects.create(**self.sensor_data)
        self.event_data.update({'sensor': s}) 
        expected = Event.objects.create(**self.event_data)
        self.event_data = {'timestamp': get_timestamp(),
                           'location': get_random_location(),
                           'status': get_status(),
                           'camera': get_camera(),
                           'avg_temp': get_avg_temp(), 
                           'avg_pressure': get_avg_pressure(), 
                           'pct_humidity': get_pct_humidity(), 
                           'altitude': get_altitude(), 
                           'windspeed': get_windspeed()}
        timestamp = get_timestamp()
        location = get_random_location()
        status = get_status()
        camera = get_camera()
        expected.timestamp = timestamp
        expected.location = location
        expected.status = status
        expected.camera = camera
        expected.save()
        actual = Event.objects.get(id=expected.id)
        self.assertEqual(timestamp, actual.timestamp)
        self.assertEqual(location, actual.location)
        self.assertEqual(status, actual.status)
        self.assertEqual(camera, actual.camera)

    def test_05_delete(self):
        s = Sensor.objects.create(**self.sensor_data)
        self.event_data.update({'sensor': s}) 
        expected = Event.objects.create(**self.event_data)
        expected.delete()
        with self.assertRaises(Event.DoesNotExist) as context:
            Event.objects.get(pk=expected.id)
        msg = 'Event matching query does not exist'
        self.assertIn(msg, str(context.exception))

    def test_06_filter(self):
        timestamps = []
        locations = []
        statuses = []
        cameras = []
        altitude = 35000
        s = Sensor.objects.create(**self.sensor_data)
        self.event_data.update({'sensor': s}) 
        expected = Event.objects.create(**self.event_data)
        for i in range(10):
            timestamps.append(get_timestamp())
            locations.append(get_random_location())
            statuses.append(get_status())
            cameras.append(get_camera())
        for idx in range(len(timestamps)):
            self.event_data.update({'timestamp': timestamps[idx],
                                    'location': locations[idx],
                                    'status': statuses[idx],
                                    'camera': cameras[idx],
                                    'altitude': altitude})
            Event.objects.create(**self.event_data)
        actual = Event.objects.filter(altitude=altitude)
        self.assertEqual(len(timestamps), len(actual))

    def test_07_save(self):
        s = Sensor.objects.create(**self.sensor_data)
        self.event_data.update({'sensor': s}) 
        expected = Event(**self.event_data)
        expected.save()
        self.assertIsNone(expected.link)
        self.assertIsNone(expected.dlink)
        self.assertIsNone(expected.ulink)
        actual = Event.objects.get(id=expected.id)
        self.assertIsNotNone(actual.link)
        self.assertIsNotNone(actual.dlink)
        self.assertIsNotNone(actual.ulink)

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

