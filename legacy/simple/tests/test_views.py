from bs4 import BeautifulSoup
from decimal import Decimal
from json import dumps, loads
from random import randint, random

from django.contrib import admin
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management import execute_from_command_line
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.test import Client, RequestFactory, TestCase

from simple.models import Widget
from simple.forms import WidgetForm
from simple.views import created, deleted, home, updated, widget_create
from simple.views import widget_delete, widget_detail, widget_list, widget_update

class TestWidgetView(TestCase):
    fixtures = ['group',
                'group_permission',
                'permission',
                'user',
                'user_groups',
                'user_permission',
                'widget']

    @classmethod
    def setUpTestData(cls):
        call_command('loaddata', 'permission', verbosity=2)
        call_command('loaddata', 'user', verbosity=2)
        call_command('loaddata', 'group', verbosity=2)
        call_command('loaddata', 'user_permission', verbosity=2)
        call_command('loaddata', 'widget', verbosity=2)

    @classmethod
    def setUpClass(cls):
        cls.kwargs = {'view': {'username': 'view',
                               'password': 'readonly'},
                      'add': {'username': 'add',
                              'password': 'write'},
                      'change': {'username': 'change',
                                 'password': 'readwrite'},
                      'delete': {'username': 'delete',
                                 'password': 'write'}}

    @classmethod
    def tearDownClass(cls):
        cls.kwargs = {}

    def setUp(self):
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
        offset = page * limit
        limit += offset
        return (offset, limit)
 
    def _set_user(self, user):
        self.data = {'username': user['username'],
                     'password': user['password']}
        self.user = User.objects.get(username=self.data['username'])
        self.user = authenticate(username=self.data['username'],
                                 password=self.data['password'])

    def _update_headers(self):
        self.headers.update({'content-length': len(dumps(self.data))})
        return

    def ttest_01_list_default_page(self):
        page = 0
        (offset, limit) = self._convert_page(page)
        self._set_user(self.kwargs['view'])
        self.assertTrue(self.user.is_authenticated())
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        url = reverse('simple:widget-list')
        self.request = self.factory.get(path=url,
                                        content_type=self.format)
        self.request.user = self.user
        response = widget_list(request=self.request)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual('Simple: Active Widgets', soup.title.string)
        expected = Widget.objects.filter(deleted=False)[offset:limit]
        rows = soup.findAll('table')[0].findAll('tbody')[0].findAll('tr')
        self.assertEqual(len(expected), len(rows))

    def ttest_02_list_first_page(self):
        page = 0
        (offset, limit) = self._convert_page(page)
        self._set_user(self.kwargs['view'])
        self.assertTrue(self.user.is_authenticated())
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        url = reverse('simple:widget-list', kwargs={'page': page})
        self.request = self.factory.get(path=url,
                                        content_type=self.format)
        self.request.user = self.user
        response = widget_list(request=self.request, page=page)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual('Simple: Active Widgets', soup.title.string)
        expected = Widget.objects.filter(deleted=False)[offset:limit]
        rows = soup.findAll('table')[0].findAll('tbody')[0].findAll('tr')
        self.assertEqual(len(expected), len(rows))

    def ttest_03_list_next_page(self):
        page = 1
        (offset, limit) = self._convert_page(page)
        self._set_user(self.kwargs['view'])
        self.assertTrue(self.user.is_authenticated())
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        url = reverse('simple:widget-list', kwargs={'page': page})
        self.request = self.factory.get(path=url,
                                        content_type=self.format)
        self.request.user = self.user
        response = widget_list(request=self.request, page=page)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual('Simple: Active Widgets', soup.title.string)
        expected = Widget.objects.filter(deleted=False)[offset:limit]
        rows = soup.findAll('table')[0].findAll('tbody')[0].findAll('tr')
        self.assertEqual(len(expected), len(rows))

    def ttest_04_detail(self):
        pk = 1
        self._set_user(self.kwargs['view'])
        self.assertTrue(self.user.is_authenticated())
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        expected = Widget.objects.get(pk=pk)
        url = reverse('simple:widget-detail', kwargs={'pk': pk})
        self.request = self.factory.get(path=url,
                                        content_type=self.format)
        self.request.user = self.user
        response = widget_detail(request=self.request, pk=pk)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual('Simple: Widget Detail', soup.title.string)
        actual = soup.findAll('table')[0].findAll('tr')[-1].findAll('td')[-2]
        self.assertEqual(expected.name, actual.string)
        actual = soup.findAll('table')[0].findAll('tr')[-1].findAll('td')[-1]
        self.assertEqual(unicode(expected.cost), actual.string)

    def _create(self):
        url = '/login/?next=/'
        response = self.c.get(path=url, headers=self.headers, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEquals(u'Legacy App Login', soup.title.string)
        token = soup.find(attrs={'name': 'csrfmiddlewaretoken'})['value']
        self.data.update({'csrfmiddlewaretoken': token})
        self._update_headers()
        response = self.c.post(path=url, data=self.data, headers=self.headers, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEquals(u'App: Legacy: Home', soup.title.string)
        url = reverse('simple:widget-create')
        response = self.c.get(path=url, headers=self.headers, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        soup = BeautifulSoup(response.content, 'html.parser')
        token = soup.find(attrs={'name': 'csrfmiddlewaretoken'})['value']
        self.assertEquals(u'Create a Widget', soup.title.string)
        _ref = randint(1000, 5000)
        data = {'name': 'Random Widget {}'.format(_ref),
                'cost': float(Decimal('%0.2f' % (_ref * 1.00 * random())))}
        data.update({'csrfmiddlewaretoken': token})
        self._update_headers()
        response = self.c.post(path=url, data=data, headers=self.headers, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEquals(u'Data Submission', soup.title.string)
        pk = int(soup.find('p').string.split()[1])
        return (soup, pk)

    def _unable_to_create(self):
        url = '/login/?next=/'
        response = self.c.get(path=url, headers=self.headers, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEquals(u'Legacy App Login', soup.title.string)
        token = soup.find(attrs={'name': 'csrfmiddlewaretoken'})['value']
        self.data.update({'csrfmiddlewaretoken': token})
        self._update_headers()
        response = self.c.post(path=url, data=self.data, headers=self.headers, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEquals(u'App: Legacy: Home', soup.title.string)
        url = reverse('simple:widget-create')
        response = self.c.get(path=url, headers=self.headers, follow=False)
        return response

    def ttest_05_create(self):
        # test using Client not FactoryRequest because auth/auth wrappers
        self._set_user(self.kwargs['add'])
        self.assertTrue(self.user.has_perm('simple.add_widget'))
        (soup, pk) = self._create()
        self.assertEqual(u'Object {} created successfully.'.format(pk),
                         soup.find('p').string)

    def ttest_06_create_insufficient_perms(self):
        self._set_user(self.kwargs['view'])
        self.assertFalse(self.user.has_perm('simple.add_widget'))
        self.assertEquals(set(), self.user.get_all_permissions())
        self.assertEquals(set(), self.user.get_group_permissions())
        response = self._unable_to_create()
        self.assertEqual(302, response.status_code)
        self.assertEqual('Found', response.reason_phrase)
        self.assertEqual('/login/?next=/simple/widgets/create/', response.url)

    def ttest_07_update(self):
        # user change has change_widget permission which includes add_widget
        self._set_user(self.kwargs['change'])
        self.assertTrue(self.user.has_perm('simple.change_widget'))
        (soup, pk) = self._create()
        self.assertEqual(u'Object {} created successfully.'.format(pk),
                         soup.find('p').string)
        url = reverse('simple:widget-update', kwargs={'pk': pk})
        response = self.c.get(path=url, headers=self.headers, follow=False)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        soup = BeautifulSoup(response.content, 'html.parser')
        token = soup.find(attrs={'name': 'csrfmiddlewaretoken'})['value']
        self.assertEquals(u'Update an Existing Widget', soup.title.string)
        name = soup.find(attrs={'id': 'id_name'})['value']
        cost = soup.find(attrs={'id': 'id_cost'})['value']
        data = {'name': 'Random Widget {}'.format(randint(1000, 5000)),
                'cost': cost}
        data.update({'csrfmiddlewaretoken': token})
        self._update_headers()
        response = self.c.post(path=url, data=data, headers=self.headers, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEquals(u'Data Modification', soup.title.string)
        pk = int(soup.find('p').string.split()[1])
        self.assertEqual(u'Object {} updated successfully.'.format(pk),
                         soup.find('p').string)

    def ttest_08_update_insufficient_perms(self):
        # user add does not have change_widget permission
        self._set_user(self.kwargs['add'])
        (soup, pk) = self._create()
        self.assertEqual(u'Object {} created successfully.'.format(pk),
                         soup.find('p').string)
        self.assertFalse(self.user.has_perm('simple.change_widget'))
        self.assertEquals(set(['simple.add_widget']), self.user.get_all_permissions())
        self.assertEquals(set(), self.user.get_group_permissions())
        url = reverse('simple:widget-list')
        response = self.c.get(path=url, headers=self.headers, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEquals(u'Simple: Active Widgets', soup.title.string)
        soup = BeautifulSoup(response.content, 'html.parser')
        url = soup.findAll('table')[0].findAll('tbody')[0].findAll('tr')[0].findAll('td')[0].string
        response = self.c.get(path=url, headers=self.headers, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        soup = BeautifulSoup(response.content, 'html.parser')
        url = soup.findAll('button')[0].find('a')['href']
        response = self.c.get(path=url, headers=self.headers, follow=False)
        self.assertEqual(302, response.status_code)
        self.assertEqual('Found', response.reason_phrase)
        self.assertEqual('/login/?next={}'.format(url), response.url)

    def ttest_09_delete_update(self):
        # user delete has delete_widget, add_widget permissions but not change_widget
        self._set_user(self.kwargs['delete'])
        self.assertTrue(self.user.has_perm('simple.delete_widget'))
        (soup, pk) = self._create()
        self.assertEqual(u'Object {} created successfully.'.format(pk),
                         soup.find('p').string)
        url = reverse('simple:widget-delete', kwargs={'pk': pk})
        response = self.c.get(path=url, headers=self.headers, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        soup = BeautifulSoup(response.content, 'html.parser')
        token = soup.find(attrs={'name': 'csrfmiddlewaretoken'})['value']
        self.assertEquals(u'Delete an Existing Widget', soup.title.string)
        name = soup.find(attrs={'id': 'id_name'})['value']
        cost = soup.find(attrs={'id': 'id_cost'})['value']
        data = {'name': name,
                'cost': cost,
                'deleted': True}
        data.update({'csrfmiddlewaretoken': token})
        self._update_headers()
        # HTTP DELETE replaced with HTTP POST to avoid CSRF
        response = self.c.post(path=url, data=data, headers=self.headers, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEquals(u'Data Deletion', soup.title.string)
        pk = int(soup.find('p').string.split()[1])
        self.assertEqual(u'Object {} deleted successfully.'.format(pk),
                         soup.find('p').string)

    def ttest_10_delete_insufficient_perms(self):
        # user add does not have delete_widget permission
        self._set_user(self.kwargs['add'])
        (soup, pk) = self._create()
        self.assertEqual(u'Object {} created successfully.'.format(pk),
                         soup.find('p').string)
        self.assertFalse(self.user.has_perm('simple.delete_widget'))
        self.assertEquals(set(['simple.add_widget']), self.user.get_all_permissions())
        self.assertEquals(set(), self.user.get_group_permissions())
        url = reverse('simple:widget-list')
        response = self.c.get(path=url, headers=self.headers, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        soup = BeautifulSoup(response.content, 'html.parser')
        url = soup.findAll('table')[0].findAll('tbody')[0].findAll('tr')[0].findAll('td')[0].string
        response = self.c.get(path=url, headers=self.headers, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        soup = BeautifulSoup(response.content, 'html.parser')
        url = soup.findAll('button')[1].find('a')['href']
        response = self.c.get(path=url, headers=self.headers, follow=False)
        self.assertEqual(302, response.status_code)
        self.assertEqual('Found', response.reason_phrase)
        self.assertEqual('/login/?next={}'.format(url), response.url)

    def ttest_11_home(self):
        self._set_user(self.kwargs['view'])
        self.assertTrue(self.user.is_authenticated())
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        url = reverse('simple:home')
        self.request = self.factory.get(path=url,
                                        content_type=self.format)
        self.request.user = self.user
        response = home(request=self.request)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual('Simple App', soup.title.string)
        self.assertEqual('Django: Simple App', soup.find('h2').string)
