from bs4 import BeautifulSoup
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
from django.test import RequestFactory, TestCase

from simple.models import Widget
from simple.forms import WidgetForm
from simple.views import created, deleted, home, updated, widget_create
from simple.views import widget_delete, widget_detail, widget_list, widget_update

class TestWidget(TestCase):
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

        #execute_from_command_line(['manage.py',
        #                           'loaddata',
        #                           'permission'])
        #execute_from_command_line(['manage.py',
        #                           'loaddata',
        #                           'user_groups'])
        #execute_from_command_line(['manage.py',
        #                           'loaddata',
        #                           'user'])
        #execute_from_command_line(['manage.py',
        #                           'loaddata',
        #                           'group'])
        #execute_from_command_line(['manage.py',
        #                           'loaddata',
        #                           'group_permission'])
        #execute_from_command_line(['manage.py',
        #                           'loaddata',
        #                           'user_permission'])
        #execute_from_command_line(['manage.py',
        #                           'loaddata',
        #                           'widget'])

    @classmethod
    def tearDownClass(cls):
        cls.kwargs = {}

    def setUp(self):
        self.factory = RequestFactory()
        self.format = 'application/json'
        self.request = None
        self.maxDiff = None
        self.data = None
        self.user = None

    def tearDown(self):
        self.factory = None
        self.format = None
        self.request = None
        self.data = None
        self.user = None

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

    def test_01_list_default_page(self):
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

    def test_02_list_first_page(self):
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

    def test_03_list_next_page(self):
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

    def test_04_detail(self):
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
        actual = soup.findAll('table')[0].findAll('tr')[-1].findAll('td')[-1]
        self.assertEqual(expected.name, actual.string)

    def _create(self):
        self.assertTrue(self.user.is_authenticated())
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        url = reverse('simple:widget-create')
        self.request = self.factory.get(path=url,
                                        content_type=self.format)
        self.request.user = self.user
        print('username: {}'.format(self.user.username))
        print('groups: {}'.format(self.user.groups))
        print('user permissions: {}'.format(self.user.user_permissions.all()))
        print('staff user: {}'.format(self.user.is_staff))
        print('super user: {}'.format(self.user.is_superuser))
        response = widget_create(request=self.request)
        self.assertEqual('Found', response.reason_phrase)
        self.assertIn('OK', response.url)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        soup = BeautifulSoup(response.content, 'html.parser')
        token = soup.find(attrs={'name': 'csrfmiddlewaretoken'})['value']
        _ref = randint(1000, 5000)
        data = {'name': 'Random Widget {}'.format(_ref),
                'cost': _ref * 1.00 * random()}
        data.update({'csrfmiddlewaretoken': token})
        self.request = self.factory.post(path=url,
                                         data=dumps(data),
                                         content_type=self.format)
        self.request.user = self.user
        self.request.POST = data
        response = widget_create(request=self.request)
        self.assertEqual(302, response.status_code)
        self.assertEqual('Found', response.reason_phrase)
        pk = int(response.url.split('/')[-2])
        self.request = self.factory.get(path=response.url,
                                        content_type=self.format)
        self.request.user = self.user
        response = created(request=self.request)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        soup = BeautifulSoup(response.content, 'html.parser')
        return (soup, pk)

    def _unable_to_create(self):
        self.assertTrue(self.user.is_authenticated())
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        url = reverse('simple:widget-create')
        self.request = self.factory.get(path=url,
                                        content_type=self.format)
        self.request.user = self.user
        response = widget_create(request=self.request)
        self.assertEqual(302, response.status_code)
        self.assertEqual('Found', response.reason_phrase)
        return response

    def test_05_create(self):
        self._set_user(self.kwargs['add'])
        (soup, pk) = self._create()
        self.assertEqual(u'Object created successfully.', soup.find('p').string)

    def test_06_create_insufficient_perms(self):
        self._set_user(self.kwargs['view'])
        response = self._unable_to_create()
        self.assertEqual('/login/?next=/simple/widgets/create/', response.url)

    def test_07_update(self):
        self._set_user(self.kwargs['change'])
        (soup, pk) = self._create()
        self.assertEqual(u'Object created successfully.', soup.find('p').string)
        url = reverse('simple:widget-update', kwargs={'pk': pk})
        self.request = self.factory.get(path=url,
                                        content_type=self.format)
        self.request.user = self.user
        response = widget_update(request=self.request, pk=pk)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        soup = BeautifulSoup(response.content, 'html.parser')
        token = soup.find(attrs={'name': 'csrfmiddlewaretoken'})['value']
        data = {'name': 'Random Widget {}'.format(randint(1000, 5000))}
        data.update({'csrfmiddlewaretoken': token})
        self.request = self.factory.post(path=url,
                                         data=dumps(data),
                                         content_type=self.format)
        self.request.user = self.user
        self.request.POST = data
        response = widget_update(request=self.request, pk=pk)
        self.assertEqual(302, response.status_code)
        self.assertEqual('Found', response.reason_phrase)
        self.request = self.factory.get(path=response.url,
                                        content_type=self.format)
        self.request.user = self.user
        response = updated(request=self.request)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(u'Object updated successfully.', soup.find('p').string)

    def test_08_update_insufficient_perms(self):
        self._set_user(self.kwargs['add'])
        response = self._unable_to_create()
        self.assertEqual('/login/?next=/simple/widgets/create/', response.url)

    def test_09_delete_update(self):
        self._set_user(self.kwargs['delete'])
        print('username: {}'.format(self.user.username))
        print('groups: {}'.format(self.user.groups))
        print('user permissions: {}'.format(self.user.user_permissions.all()))
        print('staff user: {}'.format(self.user.is_staff))
        print('super user: {}'.format(self.user.is_superuser))
        (soup, pk) = self._create()
        self.assertEqual(u'Object created successfully.', soup.find('p').string)
        url = reverse('simple:widget-delete', kwargs={'pk': pk})
        self.request = self.factory.get(path=url,
                                        content_type=self.format)
        self.request.user = self.user
        response = widget_delete(request=self.request, pk=pk)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        soup = BeautifulSoup(response.content, 'html.parser')
        token = soup.find(attrs={'name': 'csrfmiddlewaretoken'})['value']
        data = {'name': 'Random Widget {}'.format(randint(1000, 5000))}
        data.update({'deleted': True})
        data.update({'csrfmiddlewaretoken': token})
        # HTTP DELETE replaced with HTTP POST to avoid CSRF
        self.request = self.factory.post(path=url,
                                         data=dumps(data),
                                         content_type=self.format)
        self.request.user = self.user
        self.request.POST = data
        response = widget_delete(request=self.request, pk=pk)
        self.assertEqual(302, response.status_code)
        self.assertEqual('Found', response.reason_phrase)
        self.request = self.factory.get(path=response.url,
                                        content_type=self.format)
        self.request.user = self.user
        response = deleted(request=self.request)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(u'Object deleted successfully.', soup.find('p').string)

    def test_10_delete_insufficient_perms(self):
        self._set_user(self.kwargs['add'])
        response = self._unable_to_create()
        self.assertEqual('/login/?next=/simple/widgets/create/', response.url)

    def test_11_home(self):
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
