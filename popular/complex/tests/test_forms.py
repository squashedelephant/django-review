# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from bs4 import BeautifulSoup
from random import randint, random

from django.contrib.auth.models import User
from django.test import TestCase

from complex.forms import EventForm, SensorForm, SensorUpdateForm
from complex.models import Event, Sensor
from complex.tests.utils import get_alt_units, get_pressure_units
from complex.tests.utils import get_random_name, get_random_sku, get_serial_no
from complex.tests.utils import get_temp_units, get_ws_units
from complex.tests.utils import get_altitude, get_avg_pressure, get_avg_temp
from complex.tests.utils import get_camera, get_pct_humidity, get_random_location
from complex.tests.utils import get_status, get_timestamp, get_windspeed


class TestEventForm(TestCase):
    fixtures = ['event', 'sensor', 'user']

    def setUp(self):
        self.user = User.objects.get(username='qa')
        value = randint(1000, 5000)
        self.sensor_data = {'name': get_random_name(),
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

        self.data_long = self.event_data.copy()
        self.data_long.update({'location': 'Exceedingly Long {}'.format(value)})
        self.data_empty = self.event_data.copy()
        self.data_empty.update({'location': None})
        self.data_blank = self.event_data.copy()
        self.data_blank.update({'location': ''})

    def tearDown(self):
        self.sensor_data = None
        self.event_data = None
        self.data_long = None
        self.data_empty = None
        self.data_blank = None

    def test_01_sensor_unselected(self):
        form = EventForm(data=self.event_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.is_bound)
        self.assertEqual(1, len(form.errors['sensor']))
        self.assertEqual(u'This field is required.',
                         form.errors['sensor'][0])

    def test_02_sensor_selected(self):
        form = EventForm(data=self.event_data)
        soup = BeautifulSoup(str(form), 'html.parser')
        sensor = soup.find(attrs={'name': 'sensor'}).findAll('option')[1]['value']
        self.event_data.update({'sensor': sensor})
        form = EventForm(data=self.event_data)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.is_bound)
        self.assertEqual(self.event_data['sensor'],
                         form.data['sensor'])

    def test_03_timestamp_unselected(self):
        del self.event_data['timestamp']
        form = EventForm(data=self.event_data)
        soup = BeautifulSoup(str(form), 'html.parser')
        sensor = soup.find(attrs={'name': 'sensor'}).findAll('option')[1]['value']
        self.event_data.update({'sensor': sensor})
        form = EventForm(data=self.event_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.is_bound)
        self.assertEqual(1, len(form.errors['timestamp']))
        self.assertEqual(u'This field is required.',
                         form.errors['timestamp'][0])

    def test_04_timestamp_selected(self):
        form = EventForm(data=self.event_data)
        soup = BeautifulSoup(str(form), 'html.parser')
        sensor = soup.find(attrs={'name': 'sensor'}).findAll('option')[1]['value']
        timestamp = soup.find(attrs={'name': 'timestamp'})['value']
        self.event_data.update({'sensor': sensor,
                                'timestamp': timestamp})
        form = EventForm(data=self.event_data)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.is_bound)
        self.assertEqual(self.event_data['sensor'],
                         form.data['sensor'])
        self.assertEqual(self.event_data['timestamp'],
                         form.data['timestamp'])

    def test_05_location_unselected(self):
        del self.event_data['location']
        form = EventForm(data=self.event_data)
        soup = BeautifulSoup(str(form), 'html.parser')
        sensor = soup.find(attrs={'name': 'sensor'}).findAll('option')[1]['value']
        self.event_data.update({'sensor': sensor})
        form = EventForm(data=self.event_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.is_bound)
        self.assertEqual(1, len(form.errors['location']))
        self.assertEqual(u'This field is required.',
                         form.errors['location'][0])

    def test_06_location_selected(self):
        form = EventForm(data=self.event_data)
        soup = BeautifulSoup(str(form), 'html.parser')
        sensor = soup.find(attrs={'name': 'sensor'}).findAll('option')[1]['value']
        location = soup.find(attrs={'name': 'location'}).findAll('option')[1]['value']
        self.event_data.update({'sensor': sensor,
                                'location': location})
        form = EventForm(data=self.event_data)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.is_bound)
        self.assertEqual(self.event_data['sensor'],
                         form.data['sensor'])
        self.assertEqual(self.event_data['location'],
                         form.data['location'])

    def test_07_status_unselected(self):
        del self.event_data['status']
        form = EventForm(data=self.event_data)
        soup = BeautifulSoup(str(form), 'html.parser')
        sensor = soup.find(attrs={'name': 'sensor'}).findAll('option')[1]['value']
        self.event_data.update({'sensor': sensor})
        form = EventForm(data=self.event_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.is_bound)
        self.assertEqual(1, len(form.errors['status']))
        self.assertEqual(u'This field is required.',
                         form.errors['status'][0])

    def test_08_status_selected(self):
        form = EventForm(data=self.event_data)
        soup = BeautifulSoup(str(form), 'html.parser')
        sensor = soup.find(attrs={'name': 'sensor'}).findAll('option')[1]['value']
        location = soup.find(attrs={'name': 'location'}).findAll('option')[1]['value']
        status = soup.find(attrs={'name': 'status'}).findAll('option')[1]['value']
        self.event_data.update({'sensor': sensor,
                                'location': location,
                                'status': status})
        form = EventForm(data=self.event_data)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.is_bound)
        self.assertEqual(self.event_data['sensor'],
                         form.data['sensor'])
        self.assertEqual(self.event_data['location'],
                         form.data['location'])
        self.assertEqual(self.event_data['status'],
                         form.data['status'])

    def test_09_object(self):
        form = EventForm(data=self.event_data)
        self.assertIn('location', str(form))
        flds_1 = '<EventForm bound=True, valid=False, fields=(sensor;timestamp;location;'
        flds_2 = 'status;camera;avg_temp;avg_pressure;pct_humidity;altitude;windspeed)>'
        self.assertEqual('{}{}'.format(flds_1, flds_2),
                         repr(form))

class TestSensorForm(TestCase):
    fixtures = ['sensor', 'user']

    def setUp(self):
        self.user = User.objects.get(username='qa')
        value = randint(1000, 5000)
        self.data_invalid = {}
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

    def test_05_object(self):
        form = SensorForm(data=self.data_valid)
        soup = BeautifulSoup(str(form), 'html.parser')
        for option in soup.find(attrs={'name': 'created_by'}).findAll('option'):
            if option.text == self.user.username:
                self.data_valid.update({'created_by': option['value']})
        form = SensorForm(data=self.data_valid)
        self.assertIn('name', str(form))
        flds_1 = '(created_by;name;sku;serial_no;temp_units;pressure_units;'
        flds_2 = 'alt_units;ws_units;climate;camera)>'
        self.assertEqual('<SensorForm bound=True, valid=True, fields={}{}'.format(flds_1, flds_2),
                         repr(form))

    def test_06_default_errors(self):
        form = SensorForm(data=self.data_invalid)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.is_bound)
        self.assertEqual(1, len(form.errors['created_by']))
        self.assertEqual(u'This field is required.',
                         form.errors['created_by'][0])
        self.assertEqual(1, len(form.errors['name']))
        self.assertEqual(u'This field is required.',
                         form.errors['name'][0])
        self.assertEqual(1, len(form.errors['serial_no']))
        self.assertEqual(u'This field is required.',
                         form.errors['serial_no'][0])
        self.assertEqual(1, len(form.errors['temp_units']))
        self.assertEqual(u'This field is required.',
                         form.errors['temp_units'][0])
        self.assertEqual(1, len(form.errors['alt_units']))
        self.assertEqual(u'This field is required.',
                         form.errors['alt_units'][0])
        self.assertEqual(1, len(form.errors['ws_units']))
        self.assertEqual(u'This field is required.',
                         form.errors['ws_units'][0])
        self.assertEqual(1, len(form.errors['pressure_units']))
        self.assertEqual(u'This field is required.',
                         form.errors['pressure_units'][0])

class TestSensorUpdateForm(TestCase):
    fixtures = ['sensor', 'user']

    def setUp(self):
        self.user = User.objects.get(username='qa')
        value = randint(1000, 5000)
        self.data_invalid = {}
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

    def test_01_serial_no_read_only(self):
        form = SensorForm(data=self.data_valid)
        soup = BeautifulSoup(str(form), 'html.parser')
        for option in soup.find(attrs={'name': 'created_by'}).findAll('option'):
            if option.text == self.user.username:
                self.data_valid.update({'created_by': option['value']})
        form = SensorForm(data=self.data_valid)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.is_bound)
        sensor = Sensor(**form.cleaned_data)
        form = SensorUpdateForm(data=self.data_valid, instance=sensor)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.is_bound)
        soup = BeautifulSoup(str(form), 'html.parser')
        input = soup.find(attrs={'name': 'serial_no'})
        self.assertTrue(input.has_attr('disabled'))
