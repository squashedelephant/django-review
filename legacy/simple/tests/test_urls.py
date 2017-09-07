from bs4 import BeautifulSoup
from json import dumps

from django.contrib.auth.models import User
from django.core.management import execute_from_command_line
from django.http.cookie import SimpleCookie
from django.test import Client, TestCase, TransactionTestCase
from django.urls import reverse

from legacy.tests.utils import flatten_list_of_tuples

from simple.models import Widget

class TestSimpleURL(TestCase):
    fixtures = ['user']
    @classmethod
    def setUpClass(cls):
        cls.kwargs = {'active': {'username': 'active',
                                 'password': 'basicuser'},
                      'staff': {'username': 'staff',
                                'password': 'adminaccess'},
                      'superuser': {'username': 'superuser',
                                    'password': 'fullaccess'},
                      'invalid': {'username': 'invalid',
                                  'password': 'wrongguess'}}
        cls.session_keys = [u'_auth_user_id',
                            u'_auth_user_backend',
                            u'_auth_user_hash']
        cls.cookies_keys = ['sessionid']
        execute_from_command_line(['manage.py',
                                   'loaddata',
                                   'user'])
        execute_from_command_line(['manage.py',
                                   'loaddata',
                                   'widget'])
        cls.c = Client(enforce_csrf_checks=True)

    @classmethod
    def tearDownClass(cls):
        cls.kwargs = {}
        cls.session_keys = []
        cls.cookies_keys = []
        cls.c = None

    def setUp(self):
        self.format = 'application/json'
        self.maxDiff = None
        user = self.kwargs['staff']
        self.data = {'username': user['username'],
                     'password': user['password']}
        self.headers = {'connection': 'keep-alive',
                        'accept-language': 'en-US,en;q=0.8',
                        'accept-encoding': 'gzip,deflate,br',
                        'cache-control': 'max-age=0',
                        'content-type': 'application/x-www-form-urlencoded',
                        'content-length': len(dumps(self.data)),
                        'accept': 'text/html;q=0.9,image/webp,image/apng,*/*;q=0.8'}

    def tearDown(self):
        if self.c:
           self.c.logout()

    def test_01_fixtures_loaded(self):
        self.assertEqual(9, len(User.objects.all()))
        self.assertEqual(10, len(Widget.objects.all()))

    def test_02_main_page(self):
        url = '/'
        response = self.c.get(path=url, headers=self.headers, follow=False)
        self.assertEqual(302, response.status_code)
        self.assertEqual('Found', response.reason_phrase)
        response = self.c.get(path=url, headers=self.headers, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        soup = BeautifulSoup(response.content, 'html.parser')
        token = soup.find(attrs={'name': 'csrfmiddlewaretoken'})['value']
        self.data.update({'csrfmiddlewaretoken': token})
        self.assertEquals('Legacy App Login', soup.title.string)
        url = '/login/?next=/'
        response = self.c.post(path=url, data=self.data, headers=self.headers, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEquals('Welcome to App: Legacy using Simple Widgets', soup.find('h3').string)

    def test_03_login_get_cookie(self):
        url = '/login/'
        self.assertEqual(SimpleCookie, type(self.c.cookies))
        self.assertEqual(0, len(self.c.cookies))
        response = self.c.get(path=url, headers=self.headers, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        self.assertTrue(response.csrf_cookie_set)
        self.assertEqual(1, len(self.c.cookies))
        self.assertTrue(self.c.cookies.has_key('csrftoken'))

    def test_04_login_get_sessionid(self):
        url = '/login/'
        response = self.c.get(path=url, headers=self.headers, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        self.assertTrue(self.c.login(**self.data))
        self.assertTrue(response.csrf_cookie_set)
        self.assertEqual(2, len(self.c.cookies))
        self.assertTrue(self.c.cookies.has_key('csrftoken'))
        self.assertTrue(self.c.cookies.has_key('sessionid'))
        self.assertTrue(self.c.cookies.get('sessionid').value)

    def test_05_login_authenticated(self):
        url = '/login/'
        staff = self.kwargs['staff']
        user = User.objects.get(username=staff['username'])
        response = self.c.get(path=url, headers=self.headers, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        url = '/user/{}/'.format(user.id)
        response = self.c.get(path=url, headers=self.headers, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertIsNone(soup.find(name='p',
                                    text='username: {}'.format(user.username)))
        self.assertIsNone(soup.find(name='p', 
                                    text='email: {}'.format(user.email)))
        self.assertTrue(self.c.login(**self.data))
        response = self.c.get(path=url, headers=self.headers, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertIsNotNone(soup.find(name='p',
                                       text='username: {}'.format(user.username)))
        self.assertIsNotNone(soup.find(name='p',
                                       text='email: {}'.format(user.email)))

    def test_06_logout_clear_session(self):
        url = '/login/'
        response = self.c.get(path=url, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.csrf_cookie_set)
        self.assertTrue(self.c.login(**self.data))
        self.assertEqual(2, len(self.c.cookies))
        self.assertTrue(self.c.cookies.has_key('csrftoken'))
        self.assertTrue(self.c.cookies.has_key('sessionid'))
        self.assertGreater(len(self.c.cookies.get('sessionid').value), 0)
        self.c.logout()
        self.assertEqual(0, len(self.c.cookies))

    def test_07_login_active_user(self):
        url = '/login/'
        active = self.kwargs['active']
        user = User.objects.get(username=active['username'])
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        response = self.c.get(path=url, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.csrf_cookie_set)
        self.assertTrue(self.c.login(**{'username': active['username'],
                                        'password': active['password']}))
        session_items = flatten_list_of_tuples(self.c.session.items())
        for key in self.session_keys:
            self.assertIn(key, session_items)
        cookie_items = flatten_list_of_tuples(self.c.cookies.items())
        for key in self.cookies_keys:
            self.assertIn(key, cookie_items)
        url = '/user/{}/'.format(user.id)
        response = self.c.get(path=url, headers=self.headers, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertIsNotNone(soup.find(name='p',
                                       text='username: {}'.format(user.username)))
        self.assertIsNotNone(soup.find(name='p',
                                       text='email: {}'.format(user.email)))
        self.assertIsNone(self.c.logout())

    def test_08_login_staff_user(self):
        url = '/login/'
        staff = self.kwargs['staff']
        user = User.objects.get(username=staff['username'])
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_superuser)
        response = self.c.get(path=url, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.csrf_cookie_set)
        self.assertTrue(self.c.login(**{'username': staff['username'],
                                        'password': staff['password']}))
        session_items = flatten_list_of_tuples(self.c.session.items())
        for key in self.session_keys:
            self.assertIn(key, session_items)
        cookie_items = flatten_list_of_tuples(self.c.cookies.items())
        for key in self.cookies_keys:
            self.assertIn(key, cookie_items)
        url = '/user/{}/'.format(user.id)
        response = self.c.get(path=url, headers=self.headers, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertIsNotNone(soup.find(name='p',
                                       text='username: {}'.format(user.username)))
        self.assertIsNotNone(soup.find(name='p',
                                       text='email: {}'.format(user.email)))
        self.assertIsNone(self.c.logout())

    def test_09_login_superuser_user(self):
        url = '/login/'
        superuser = self.kwargs['superuser']
        user = User.objects.get(username=superuser['username'])
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        response = self.c.get(path=url, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.csrf_cookie_set)
        self.assertTrue(self.c.login(**{'username': superuser['username'],
                                        'password': superuser['password']}))
        session_items = flatten_list_of_tuples(self.c.session.items())
        for key in self.session_keys:
            self.assertIn(key, session_items)
        cookie_items = flatten_list_of_tuples(self.c.cookies.items())
        for key in self.cookies_keys:
            self.assertIn(key, cookie_items)
        url = '/user/{}/'.format(user.id)
        response = self.c.get(path=url, headers=self.headers, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertIsNotNone(soup.find(name='p',
                                       text='username: {}'.format(user.username)))
        self.assertIsNotNone(soup.find(name='p',
                                       text='email: {}'.format(user.email)))
        self.assertIsNone(self.c.logout())

    def test_10_login_invalid_user(self):
        url = '/login/'
        invalid = self.kwargs['invalid']
        response = self.c.get(path=url, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.csrf_cookie_set)
        self.assertFalse(self.c.login(**{'username': invalid['username'],
                                        'password': invalid['password']}))

    def test_11_real_login_logout(self):
        url = '/login/'
        response = self.c.get(path=url, headers=self.headers, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        soup = BeautifulSoup(response.content, 'html.parser')
        token = soup.find(attrs={'name': 'csrfmiddlewaretoken'})['value']
        self.data.update({'csrfmiddlewaretoken': token})
        url = '/login/?next=/'
        response = self.c.post(path=url, data=self.data, headers=self.headers, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(u'App: Legacy: Home', soup.title.string)
        url = '/logout/'
        response = self.c.get(path=url, headers=self.headers, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)

    def test_13_home_URL(self):
        url = '/'
        response = self.c.get(path=url, headers=self.headers, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual('Legacy App Login', soup.find('title').text)
