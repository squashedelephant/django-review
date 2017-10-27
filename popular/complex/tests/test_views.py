from bs4 import BeautifulSoup
from decimal import Decimal
from json import dumps, loads
from random import randint, random

from django.contrib import admin
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group, Permission, User
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.test import Client, RequestFactory, TestCase

from complex.models import Event, Sensor
from complex.forms import EventForm, SensorForm
from complex.views import SensorCreateView, SensorDeleteView, SensorDetailView
from complex.views import SensorListView, SensorUpdateView
from complex.tests.utils import get_alt_units, get_pressure_units
from complex.tests.utils import get_random_name, get_random_sku, get_serial_no
from complex.tests.utils import get_temp_units, get_ws_units
from complex.tests.utils import get_altitude, get_avg_pressure, get_avg_temp
from complex.tests.utils import get_camera, get_pct_humidity, get_random_location
from complex.tests.utils import get_status, get_timestamp, get_windspeed

class TestSensorView(TestCase):
    fixtures = ['sensor', 'user']

    def setUp(self):
        self.kwargs = {'view': {'username': 'view',
                                'password': 'readonly'},
                       'add': {'username': 'add',
                               'password': 'write'},
                       'change': {'username': 'change',
                                  'password': 'readwrite'},
                       'delete': {'username': 'delete',
                                  'password': 'write'},
                       'qa': {'username': 'qa',
                              'password': 'br0k3nc0d3'}}
        self.factory = RequestFactory()
        self.c = Client(enforce_csrf_check=True)
        self.format = 'application/json'
        self.request = None
        self.maxDiff = None
        self.data = None
        self.user = None
        self.headers = {'connection': 'keep-alive',
                        'accept-language': 'en-US,en;q=0.8',
                        'accept-encoding': 'gzip,deflate,br',
                        'cache-control': 'max-age=0',
                        'content-type': 'application/x-www-form-urlencoded',
                        'accept': 'text/html;q=0.9,image/webp,image/apng,*/*;q=0.8'}
        self.data = {'name': get_random_name(),
                     'sku': get_random_sku(),
                     'serial_no': get_serial_no()}

    def tearDown(self):
        self.factory = None
        if self.c:
            url = '/logout/'
            response = self.c.get(path=url, headers=self.headers, follow=True)
            self.assertEqual(200, response.status_code)
            self.assertEqual('OK', response.reason_phrase)
            self.c = None
        self.format = None
        self.request = None
        self.data = None
        self.user = None
        self.headers = None

    def _convert_page(self, page):
        limit = 5
        if page == 1:
            offset = 0
            return (offset, limit)
        else:
            offset = ((page - 1) * limit)
            limit *= page
            return (offset, limit)
            
        limit = 5
        offset = (page * limit) + page
        limit += offset
        return (offset, limit)

    def _set_user(self, user):
        data = {'username': user['username'],
                'password': user['password']}
        self.user = User.objects.get(username=data['username'])
        self.user = authenticate(username=data['username'],
                                 password=data['password'])
        self.data.update({'created_by': self.user.id})

    def _update_headers(self):
        self.headers.update({'content-length': len(dumps(self.data))})
        return

    def test_00_fixtures_loaded(self):
        users = User.objects.all()
        self.assertEqual(6, len(users))
        sensors = Sensor.objects.all()
        self.assertEqual(9, len(sensors))

    def test_01_list_default_page(self):
        page = 1
        (offset, limit) = self._convert_page(page)
        self._set_user(self.kwargs['qa'])
        self.assertTrue(self.user.is_authenticated())
        url = reverse('complex:sensor-list')
        self.request = self.factory.get(path=url,
                                        content_type=self.format)
        self.request.user = self.user
        response = SensorListView.as_view()(request=self.request)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        response.render()
        soup = BeautifulSoup(response.content, 'html.parser')
        expected = Sensor.objects.filter(created_by=self.request.user)[offset:limit]
        self.assertEqual('Active Sensors', soup.find('h3').string)
        rows = soup.findAll('table')[0].findAll('tbody')[0].findAll('tr')
        self.assertEqual(len(expected), len(rows))
        for idx in range(len(rows)):
            data = rows[idx].findAll('td')
            self.assertEqual(expected[idx].link, data[0].string)
            self.assertEqual(expected[idx].name, data[1].string)
            self.assertEqual(expected[idx].sku, data[2].string)
            self.assertEqual(expected[idx].serial_no, data[3].string)

    def test_02_list_first_page(self):
        page = 1
        (offset, limit) = self._convert_page(page)
        self._set_user(self.kwargs['qa'])
        self.assertTrue(self.user.is_authenticated())
        url = reverse('complex:sensor-list', kwargs={'page': page})
        self.request = self.factory.get(path=url,
                                        content_type=self.format)
        self.request.user = self.user
        response = SensorListView.as_view()(request=self.request,
                                            kwargs={'page': page})
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        response.render()
        soup = BeautifulSoup(response.content, 'html.parser')
        expected = Sensor.objects.filter(created_by=self.request.user)[offset:limit]
        self.assertEqual('Active Sensors', soup.find('h3').string)
        rows = soup.findAll('table')[0].findAll('tbody')[0].findAll('tr')
        self.assertEqual(len(expected), len(rows))
        for idx in range(len(rows)):
            data = rows[idx].findAll('td')
            self.assertEqual(expected[idx].link, data[0].string)
            self.assertEqual(expected[idx].name, data[1].string)
            self.assertEqual(expected[idx].sku, data[2].string)
            self.assertEqual(expected[idx].serial_no, data[3].string)

    def ttest_03_list_next_page(self):
        page = 2
        (offset, limit) = self._convert_page(page)
        self._set_user(self.kwargs['qa'])
        self.assertTrue(self.user.is_authenticated())
        url = reverse('complex:sensor-list', kwargs={'page': page})
        self.request = self.factory.get(path=url,
                                        content_type=self.format)
        self.request.user = self.user
        response = SensorListView.as_view()(request=self.request,
                                            kwargs={'page': page})
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        response.render()
        soup = BeautifulSoup(response.content, 'html.parser')
        expected = Sensor.objects.filter(created_by=self.request.user)[offset:limit]
        self.assertEqual('Active Sensors', soup.find('h3').string)
        rows = soup.findAll('table')[0].findAll('tbody')[0].findAll('tr')
        self.assertEqual(len(expected), len(rows))
        for idx in range(len(rows)):
            data = rows[idx].findAll('td')
            self.assertEqual(expected[idx].link, data[0].string)
            self.assertEqual(expected[idx].name, data[1].string)
            self.assertEqual(expected[idx].sku, data[2].string)
            self.assertEqual(expected[idx].serial_no, data[3].string)

    def ttest_04_detail(self):
        pk = 1
        self._set_user(self.kwargs['qa'])
        self.assertTrue(self.user.is_authenticated())
        expected = Sensor.objects.get(pk=pk)
        url = reverse('complex:sensor-detail', kwargs={'pk': expected.pk})
        self.request = self.factory.get(path=url,
                                        content_type=self.format)
        self.request.user = self.user
        response = SensorDetailView.as_view()(request=self.request,
                                              kwargs={'pk': pk})
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual('Complex: Sensor Detail', soup.title.string)
        row = soup.find(attrs={'id': 'detail'}).findAll('tr')[-1]
        self.assertEqual(expected.name, row.findAll('td')[0].string)
        self.assertEqual(expected.location, row.findAll('td')[1].string)

    def ttest_05_create(self):
        self._set_user(self.kwargs['qa'])
        self.assertTrue(self.user.is_authenticated())
        url = reverse('complex:sensor-create')
        self.request = self.factory.get(path=url,
                                        content_type=self.format,
                                        header=self.headers)
        self.request.user = self.user
        response = SensorCreateView.as_view()(request=self.request)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        response.render()
        soup = BeautifulSoup(response.content, 'html.parser')
        token = soup.find(attrs={'name': 'csrfmiddlewaretoken'})['value']
        for option in soup.find(attrs={'name': 'created_by'}).findAll('option'):
            if option.text == self.user.username:
                created_by = option['value']
        for option in soup.find(attrs={'name': 'created_by'}).findAll('option'):
            if option.text == self.user.username:
                created_by = option['value']
        for option in soup.find(attrs={'name': 'temp_units'}).findAll('option'):
            if option.has_attr('selected'):
                temp_units = option['value']
        for option in soup.find(attrs={'name': 'pressure_units'}).findAll('option'):
            if option.has_attr('selected'):
                pressure_units = option['value']
        for option in soup.find(attrs={'name': 'alt_units'}).findAll('option'):
            if option.has_attr('selected'):
                alt_units = option['value']
        for option in soup.find(attrs={'name': 'ws_units'}).findAll('option'):
            if option.has_attr('selected'):
                ws_units = option['value']
        self.data.update({'csrfmiddlewaretoken': token,
                          'created_by': created_by,
                          'temp_units': temp_units,
                          'pressure_units': pressure_units,
                          'alt_units': alt_units,
                          'ws_units': ws_units})
        print('POST data: {}'.format(self.data))
        self._update_headers()
        self.request = self.factory.post(path=url,
                                         data=self.data,
                                         content_type=self.format,
                                         header=self.headers,
                                         follow=True)
        self.request.user = self.user
        response = SensorCreateView.as_view()(request=self.request)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        response.render()
        soup = BeautifulSoup(response.content, 'html.parser')
        print(soup.prettify())
        self.assertTrue(False)
