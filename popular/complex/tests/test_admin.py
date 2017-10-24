# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from bs4 import BeautifulSoup
from json import dumps

from django.contrib.admin.sites import AdminSite
from django.contrib.admin.options import ModelAdmin
from django.contrib.auth.models import User
from django.test import Client, TestCase

from complex.admin import EventAdmin, SensorAdmin
from complex.models import Event, Sensor
from complex.tests.utils import get_alt_units, get_pressure_units
from complex.tests.utils import get_random_name, get_random_sku, get_serial_no
from complex.tests.utils import get_temp_units, get_ws_units
from complex.tests.utils import get_altitude, get_avg_pressure, get_avg_temp
from complex.tests.utils import get_camera, get_pct_humidity, get_random_location
from complex.tests.utils import get_status, get_timestamp, get_windspeed

class MockRequest:
    pass

class MockSuperUser:
    def has_perm(self, perm):
        return True

class TestEventAdmin(TestCase):
    fixtures = ['user']

    def setUp(self):
        self.maxDiff = None
        self.data = {'username': 'superuser',
                     'password': 'fullaccess'}
        self.headers = {'connection': 'keep-alive',
                        'accept-language': 'en-US,en;q=0.8',
                        'accept-encoding': 'gzip,deflate,br',
                        'cache-control': 'max-age=0',
                        'content-type': 'application/x-www-form-urlencoded',
                        'content-length': len(dumps(self.data)),
                        'accept': 'text/html;q=0.9,image/webp,image/apng,*/*;q=0.8'}
        self.c = Client(enforce_csrf_check=True)
        self.site = AdminSite()
        self.request = MockRequest()
        self.request.user = MockSuperUser()

    def tearDown(self):
        self.data = {}
        self.headers = {}
        self.c = None
        self.site = None
        self.request = None

    def test_01_event_visible(self):
        url = '/admin/'
        user = User.objects.get(username=self.data['username'])
        response = self.c.get(path=url, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.csrf_cookie_set)
        self.assertTrue(self.c.login(**self.data))
        url = '/admin/complex/event/'
        response = self.c.get(path=url, headers=self.headers, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual('Select event to change | Django site admin',
                         soup.title.string)
        self.assertIsNone(self.c.logout())

    def test_02_event_list_display(self):
        list_display = ('sensor', 'timestamp', 'location', 'status',
                        'camera', 'avg_temp', 'avg_pressure', 'pct_humidity',
                        'altitude', 'windspeed')
        self.assertTupleEqual(list_display, EventAdmin.list_display)

    def test_03_event_list_filter(self):
        list_filter = ('sensor', 'location')
        self.assertTupleEqual(list_filter, EventAdmin.list_filter)

    def test_04_event_search_fields(self):
        search_fields = ('sensor', 'timestamp', 'location', 'status')
        self.assertTupleEqual(search_fields, EventAdmin.search_fields)

    def test_05_event_fields(self):
        fields = ('sensor', 'timestamp', 'location', 'status', 'camera',
                  'avg_temp', 'avg_pressure', 'pct_humidity', 'altitude',
                  'windspeed')
        self.assertTupleEqual(fields, EventAdmin.fields)

    def test_06_event_date_hierarchy(self):
        date_hierarchy = 'timestamp'
        self.assertEqual(date_hierarchy, EventAdmin.date_hierarchy)

    def test_07_event_ordering(self):
        ordering = ('-timestamp',)
        self.assertTupleEqual(ordering, EventAdmin.ordering)

    def test_08_event_base_fields(self):
        ma = ModelAdmin(Event, self.site)
        base_fields = ['sensor', 'timestamp', 'location', 'status', 'camera',
                       'avg_temp', 'avg_pressure', 'pct_humidity', 'altitude',
                       'windspeed', 'deleted', 'link', 'ulink', 'dlink']
        self.assertListEqual(base_fields,
                             list(ma.get_form(self.request).base_fields))

    def test_09_model_registered(self):
        ma = ModelAdmin(Event, self.site)
        self.assertEqual(str(ma), 'complex.ModelAdmin')

    def test_10_model_not_registered(self):
        self.assertFalse(self.site.is_registered(EventAdmin))

    def test_11_model_fields(self):
        ma = ModelAdmin(Event, self.site)
        fields = ['sensor', 'timestamp', 'location', 'status', 'camera',
                  'avg_temp', 'avg_pressure', 'pct_humidity', 'altitude',
                  'windspeed', 'deleted', 'link', 'ulink', 'dlink']
        self.assertListEqual(fields,
                             list(ma.get_fields(self.request)))

    def test_12_model_lookup(self):
        ma = ModelAdmin(Event, self.site)
        self.assertTrue(ma.lookup_allowed('location', 'smalltown'))

class TestSensorAdmin(TestCase):
    fixtures = ['user']

    def setUp(self):
        self.maxDiff = None
        self.data = {'username': 'superuser',
                     'password': 'fullaccess'}
        self.headers = {'connection': 'keep-alive',
                        'accept-language': 'en-US,en;q=0.8',
                        'accept-encoding': 'gzip,deflate,br',
                        'cache-control': 'max-age=0',
                        'content-type': 'application/x-www-form-urlencoded',
                        'content-length': len(dumps(self.data)),
                        'accept': 'text/html;q=0.9,image/webp,image/apng,*/*;q=0.8'}
        self.c = Client(enforce_csrf_check=True)
        self.site = AdminSite()
        self.request = MockRequest()
        self.request.user = MockSuperUser()

    def tearDown(self):
        self.data = {}
        self.headers = {}
        self.c = None
        self.site = None
        self.request = None

    def test_01_sensor_visible(self):
        url = '/admin/'
        user = User.objects.get(username=self.data['username'])
        response = self.c.get(path=url, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.csrf_cookie_set)
        self.assertTrue(self.c.login(**self.data))
        url = '/admin/complex/sensor/'
        response = self.c.get(path=url, headers=self.headers, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual('Select sensor to change | Django site admin',
                         soup.title.string)
        self.assertIsNone(self.c.logout())

    def test_02_sensor_list_display(self):
        list_display = ('created_by', 'name', 'sku', 'serial_no', 'temp_units',
                        'pressure_units', 'alt_units', 'ws_units', 'installed',
                        'climate', 'camera')
        self.assertTupleEqual(list_display, SensorAdmin.list_display)

    def test_03_sensor_list_filter(self):
        list_filter = ('name', 'sku', 'installed')
        self.assertTupleEqual(list_filter, SensorAdmin.list_filter)

    def test_04_sensor_search_fields(self):
        search_fields = ('created_by', 'name', 'sku', 'serial_no', 'installed')
        self.assertTupleEqual(search_fields, SensorAdmin.search_fields)

    def test_05_sensor_fields(self):
        fields = ('created_by', 'name', 'sku', 'serial_no', 'temp_units',
                  'pressure_units', 'alt_units', 'ws_units', 'climate',
                  'camera')
        self.assertTupleEqual(fields, SensorAdmin.fields)

    def test_06_sensor_base_fields(self):
        ma = ModelAdmin(Sensor, self.site)
        base_fields = ['created_by', 'name', 'sku', 'serial_no', 'temp_units',
                       'pressure_units', 'alt_units', 'ws_units', 'climate',
                       'camera', 'link', 'ulink', 'dlink']
        self.assertListEqual(base_fields,
                             list(ma.get_form(self.request).base_fields))

    def test_07_model_registered(self):
        ma = ModelAdmin(Sensor, self.site)
        self.assertEqual(str(ma), 'complex.ModelAdmin')

    def test_08_model_not_registered(self):
        self.assertFalse(self.site.is_registered(SensorAdmin))

    def test_09_model_fields(self):
        ma = ModelAdmin(Sensor, self.site)
        fields = ['created_by', 'name', 'sku', 'serial_no', 'temp_units',
                  'pressure_units', 'alt_units', 'ws_units', 'climate',
                  'camera', 'link', 'ulink', 'dlink']
        self.assertListEqual(fields,
                             list(ma.get_fields(self.request)))

    def test_10_model_lookup(self):
        ma = ModelAdmin(Sensor, self.site)
        self.assertTrue(ma.lookup_allowed('name', 'abc'))
