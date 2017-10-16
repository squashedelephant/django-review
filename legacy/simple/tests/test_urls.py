from bs4 import BeautifulSoup
from json import dumps

from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.urlresolvers import reverse, reverse_lazy
from django.http.cookie import SimpleCookie
from django.test import Client, TestCase, TransactionTestCase
from django.urls import reverse

from legacy.tests.utils import flatten_list_of_tuples

from simple.models import Inventory, Store, Widget

class TestSimpleURL(TestCase):
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
        self.assertEqual(9, len(users))

    def test_01_login_logout(self):
        for user in self.kwargs:
            url = '/login/?next=/'
            response = self.c.get(path=url, headers=self.headers, follow=True)
            self.assertEqual(200, response.status_code)
            self.assertEqual('OK', response.reason_phrase)
            soup = BeautifulSoup(response.content, 'html.parser')
            token = soup.find(attrs={'name': 'csrfmiddlewaretoken'})['value']
            self.assertEquals('Legacy App Login', soup.title.string)
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
            self.assertEqual(u'App: Legacy: Home', soup.title.string)
            url = '/logout/'
            response = self.c.get(path=url, headers=self.headers, follow=True)
            self.assertEqual(200, response.status_code)
            self.assertEqual('OK', response.reason_phrase)

    def test_02_home(self):
        expected = '/simple/'
        self.assertEqual(expected, reverse('simple:home'))
        self.assertEqual(expected, reverse_lazy('simple:home'))

    def test_03_created(self):
        expected = '/simple/created/1/'
        self.assertEqual(expected, reverse('simple:created',
                                           kwargs={'pk': 1}))
        self.assertEqual(expected, reverse_lazy('simple:created',
                                                kwargs={'pk': 1}))

    def test_04_deleted(self):
        expected = '/simple/deleted/1/'
        self.assertEqual(expected, reverse('simple:deleted',
                                           kwargs={'pk': 1}))
        self.assertEqual(expected, reverse_lazy('simple:deleted',
                                                kwargs={'pk': 1}))

    def test_05_eperm(self):
        expected = '/simple/eperm/1/'
        self.assertEqual(expected, reverse('simple:eperm',
                                           kwargs={'pk': 1}))
        self.assertEqual(expected, reverse_lazy('simple:eperm',
                                                kwargs={'pk': 1}))

    def test_06_nonexistent(self):
        expected = '/simple/nonexistent/1/'
        self.assertEqual(expected, reverse('simple:non-existent',
                                           kwargs={'pk': 1}))
        self.assertEqual(expected, reverse_lazy('simple:non-existent',
                                                kwargs={'pk': 1}))

    def test_07_updated(self):
        expected = '/simple/updated/1/'
        self.assertEqual(expected, reverse('simple:updated',
                                           kwargs={'pk': 1}))
        self.assertEqual(expected, reverse_lazy('simple:updated',
                                                kwargs={'pk': 1}))

class TestInventoryURL(TestCase):
    def test_01_aggr(self):
        expected = '/simple/inventory/aggr/'
        self.assertEqual(expected, reverse('simple:inventory-aggr'))
        self.assertEqual(expected, reverse_lazy('simple:inventory-aggr'))
        expected = '/simple/inventory/aggr/page/0/'
        self.assertEqual(expected, reverse('simple:inventory-aggr',
                                           kwargs={'page': 0}))
        self.assertEqual(expected, reverse_lazy('simple:inventory-aggr',
                                                kwargs={'page': 0}))

    def test_02_create(self):
        expected = '/simple/inventory/create/'
        user = User.objects.get(username='add')
        self.assertEqual(expected, reverse('simple:inventory-create'))
        self.assertEqual(expected, reverse_lazy('simple:inventory-create'))

    def test_03_delete(self):
        expected = '/simple/inventory/delete/1/'
        self.assertEqual(expected, reverse('simple:inventory-delete',
                                           kwargs={'pk': 1}))
        self.assertEqual(expected, reverse_lazy('simple:inventory-delete',
                                                kwargs={'pk': 1}))

    def test_04_detail(self):
        expected = '/simple/inventory/1/'
        self.assertEqual(expected, reverse('simple:inventory-detail',
                                           kwargs={'pk': 1}))
        self.assertEqual(expected, reverse_lazy('simple:inventory-detail',
                                                kwargs={'pk': 1}))

    def test_05_list(self):
        expected = '/simple/inventory/'
        self.assertEqual(expected, reverse('simple:inventory-list'))
        self.assertEqual(expected, reverse_lazy('simple:inventory-list'))
        expected = '/simple/inventory/page/1/'
        self.assertEqual(expected, reverse('simple:inventory-list',
                                           kwargs={'page': 1}))
        self.assertEqual(expected, reverse_lazy('simple:inventory-list',
                                                kwargs={'page': 1}))

    def test_06_update(self):
        expected = '/simple/inventory/update/1/'
        self.assertEqual(expected, reverse('simple:inventory-update',
                                           kwargs={'pk': 1}))
        self.assertEqual(expected, reverse_lazy('simple:inventory-update',
                                                kwargs={'pk': 1}))

class TestStoreURL(TestCase):
    def test_01_create(self):
        expected = '/simple/stores/create/'
        user = User.objects.get(username='add')
        self.assertEqual(expected, reverse('simple:store-create'))
        self.assertEqual(expected, reverse_lazy('simple:store-create'))

    def test_02_delete(self):
        expected = '/simple/stores/delete/1/'
        self.assertEqual(expected, reverse('simple:store-delete',
                                           kwargs={'pk': 1}))
        self.assertEqual(expected, reverse_lazy('simple:store-delete',
                                                kwargs={'pk': 1}))

    def test_03_detail(self):
        expected = '/simple/stores/1/'
        self.assertEqual(expected, reverse('simple:store-detail',
                                           kwargs={'pk': 1}))
        self.assertEqual(expected, reverse_lazy('simple:store-detail',
                                                kwargs={'pk': 1}))

    def test_04_list(self):
        expected = '/simple/stores/'
        self.assertEqual(expected, reverse('simple:store-list'))
        self.assertEqual(expected, reverse_lazy('simple:store-list'))
        expected = '/simple/stores/page/1/'
        self.assertEqual(expected, reverse('simple:store-list',
                                           kwargs={'page': 1}))
        self.assertEqual(expected, reverse_lazy('simple:store-list',
                                                kwargs={'page': 1}))

    def test_05_update(self):
        expected = '/simple/stores/update/1/'
        self.assertEqual(expected, reverse('simple:store-update',
                                           kwargs={'pk': 1}))
        self.assertEqual(expected, reverse_lazy('simple:store-update',
                                                kwargs={'pk': 1}))

class TestWidgetURL(TestCase):
    def test_01_aggr(self):
        expected = '/simple/widgets/aggr/'
        self.assertEqual(expected, reverse('simple:widget-aggr'))
        self.assertEqual(expected, reverse_lazy('simple:widget-aggr'))
        expected = '/simple/widgets/aggr/page/0/'
        self.assertEqual(expected, reverse('simple:widget-aggr',
                                           kwargs={'page': 0}))
        self.assertEqual(expected, reverse_lazy('simple:widget-aggr',
                                                kwargs={'page': 0}))

    def test_02_create(self):
        expected = '/simple/widgets/create/'
        user = User.objects.get(username='add')
        self.assertEqual(expected, reverse('simple:widget-create'))
        self.assertEqual(expected, reverse_lazy('simple:widget-create'))

    def test_03_delete(self):
        expected = '/simple/widget/delete/1/'
        self.assertEqual(expected, reverse('simple:widget-delete',
                                           kwargs={'pk': 1}))
        self.assertEqual(expected, reverse_lazy('simple:widget-delete',
                                                kwargs={'pk': 1}))

    def test_04_detail(self):
        expected = '/simple/widgets/1/'
        self.assertEqual(expected, reverse('simple:widget-detail',
                                           kwargs={'pk': 1}))
        self.assertEqual(expected, reverse_lazy('simple:widget-detail',
                                                kwargs={'pk': 1}))

    def test_05_list(self):
        expected = '/simple/widgets/'
        self.assertEqual(expected, reverse('simple:widget-list'))
        self.assertEqual(expected, reverse_lazy('simple:widget-list'))
        expected = '/simple/widgets/page/1/'
        self.assertEqual(expected, reverse('simple:widget-list',
                                           kwargs={'page': 1}))
        self.assertEqual(expected, reverse_lazy('simple:widget-list',
                                                kwargs={'page': 1}))

    def test_06_update(self):
        expected = '/simple/widgets/update/1/'
        self.assertEqual(expected, reverse('simple:widget-update',
                                           kwargs={'pk': 1}))
        self.assertEqual(expected, reverse_lazy('simple:widget-update',
                                                kwargs={'pk': 1}))

