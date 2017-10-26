from bs4 import BeautifulSoup
from json import dumps

from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.urlresolvers import reverse, reverse_lazy
from django.http.cookie import SimpleCookie
from django.test import Client, TestCase, TransactionTestCase
from django.urls import reverse

class TestAuthenticationURL(TestCase):
    fixtures = ['user']

    @classmethod
    def setUpTestData(cls):
        cls.kwargs = {'add': {'username': 'add',
                              'password': 'write'},
                      'change': {'username': 'change',
                                 'password': 'readwrite'},
                      'delete': {'username': 'delete',
                                 'password': 'write'}}
        cls.session_keys = [u'_auth_user_id',
                            u'_auth_user_backend',
                            u'_auth_user_hash']
        cls.cookies_keys = ['sessionid']
        cls.c = Client(enforce_csrf_checks=True)

    @classmethod
    def tearDownTestData(cls):
        cls.kwargs = {}
        cls.session_keys = []
        cls.cookies_keys = []
        cls.c = None

    def setUp(self):
        self.format = 'application/json'
        self.maxDiff = None
        self.data = None
        self.headers = {'connection': 'keep-alive',
                        'accept-language': 'en-US,en;q=0.8',
                        'accept-encoding': 'gzip,deflate,br',
                        'cache-control': 'max-age=0',
                        'content-type': 'application/x-www-form-urlencoded',
                        'accept': 'text/html;q=0.9,image/webp,image/apng,*/*;q=0.8'}

    def tearDown(self):
        if self.c:
           self.c.logout()

    def _update_headers(self):
        self.headers.update({'content-length': len(dumps(self.data))})
        return

    def test_00_fixtures_loaded(self):
        users = User.objects.all()
        self.assertEqual(6, len(users))

    def test_01_login_logout(self):
        for user in self.kwargs:
            url = '/login/?next=/'
            response = self.c.get(path=url, headers=self.headers, follow=True)
            self.assertEqual(200, response.status_code)
            self.assertEqual('OK', response.reason_phrase)
            soup = BeautifulSoup(response.content, 'html.parser')
            token = soup.find(attrs={'name': 'csrfmiddlewaretoken'})['value']
            self.assertEquals('Popular App Login', soup.title.string)
            self.data = self.kwargs[user]
            self.data.update({'csrfmiddlewaretoken': token})
            self._update_headers()
            response = self.c.post(path=url,
                                   data=self.data,
                                   headers=self.headers,
                                   follow=True)
            self.assertEqual(200, response.status_code)
            self.assertEqual('OK', response.reason_phrase)
            soup = BeautifulSoup(response.content, 'html.parser')
            self.assertEqual(u'App: Popular: Home', soup.title.string)
            url = '/logout/'
            response = self.c.get(path=url, headers=self.headers, follow=True)
            self.assertEqual(200, response.status_code)
            self.assertEqual('OK', response.reason_phrase)
