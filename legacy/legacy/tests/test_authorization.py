from django.contrib.auth.models import User
from django.core.management import execute_from_command_line
from django.test import Client, TestCase

class TestAuthorization(TestCase):
    fixtures = ['user']
    @classmethod
    def setUpClass(cls):
        cls.kwargs = {'active': {'username': 'active',
                                 'password': 'basicuser'},
                      'staff': {'username': 'staff',
                                'password': 'adminaccess'},
                      'superuser': {'username': 'superuser',
                                    'password': 'fullaccess'}}
        cls.session_keys = [u'_auth_user_id', u'_auth_user_backend', u'_auth_user_hash']
        cls.cookies_keys = ['sessionid']
        execute_from_command_line(['manage.py', 'loaddata', 'user'])
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
        self.headers = {'connection': 'keep-alive',
                        'accept-language': 'en-US,en;q=0.8',
                        'accept-encoding': 'gzip,deflate,br',
                        'cache-control': 'max-age=0',
                        'content-type': 'application/x-www-form-urlencoded',
                        'accept': 'text/html;q=0.9,image/webp,image/apng,*/*;q=0.8'}

    def tearDown(self):
        if self.c:
           self.c.logout()

    def test_01_fixtures_loaded(self):
        self.assertEqual(9, len(User.objects.all()))

    def test_02_login_active_authorized(self):
        active = self.kwargs['active']
        user = User.objects.get(username=active['username'])
        self.assertFalse(user.has_perm('add_user'))
        self.assertFalse(user.has_perm('change_user'))
        self.assertFalse(user.has_perm('delete_user'))

    def test_03_login_staff_authorized(self):
        staff = self.kwargs['staff']
        user = User.objects.get(username=staff['username'])
        self.assertFalse(user.has_perm('add_user'))
        self.assertFalse(user.has_perm('change_user'))
        self.assertFalse(user.has_perm('delete_user'))

    def test_04_login_superuser_authorized(self):
        superuser = self.kwargs['superuser']
        user = User.objects.get(username=superuser['username'])
        self.assertTrue(user.has_perm('add_user'))
        self.assertTrue(user.has_perm('change_user'))
        self.assertTrue(user.has_perm('delete_user'))
