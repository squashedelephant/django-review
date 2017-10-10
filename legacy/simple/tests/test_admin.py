# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from bs4 import BeautifulSoup
from json import dumps

from django.contrib.admin.sites import AdminSite
from django.contrib.admin.options import ModelAdmin
from django.contrib.auth.models import User
from django.test import Client, TestCase

from simple.admin import InventoryAdmin, StoreAdmin, WidgetAdmin
from simple.models import Inventory, Store, Widget

class MockRequest:
    pass

class MockSuperUser:
    def has_perm(self, perm):
        return True

class TestInventoryAdmin(TestCase):
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

    def test_01_store_visible(self):
        url = '/admin/'
        user = User.objects.get(username=self.data['username'])
        response = self.c.get(path=url, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.csrf_cookie_set)
        self.assertTrue(self.c.login(**self.data))
        url = '/admin/simple/inventory/'
        response = self.c.get(path=url, headers=self.headers, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual('Select inventory to change | Django site admin', soup.title.string)
        self.assertIsNone(self.c.logout())

    def test_02_inventory_list_display(self):
        list_display = ('store', 'widget', 'quantity', 'created_by')
        self.assertTupleEqual(list_display, InventoryAdmin.list_display)

    def test_03_inventory_search_fields(self):
        search_fields = ('store', 'widget')
        self.assertTupleEqual(search_fields, InventoryAdmin.search_fields)

    def test_04_inventory_fields(self):
        fields = ('store', 'widget', 'quantity', 'created_by')
        self.assertTupleEqual(fields, InventoryAdmin.fields)

    def test_05_model_registered(self):
        ma = ModelAdmin(Inventory, self.site)
        self.assertEqual(str(ma), 'simple.ModelAdmin')
        
    def test_06_model_not_registered(self):
        self.assertFalse(self.site.is_registered(InventoryAdmin))

    def test_07_base_fields(self):
        ma = ModelAdmin(Inventory, self.site)
        base_fields = ['created_by', 'store', 'widget', 'quantity', 'deleted', 'link', 'ulink', 'dlink']
        self.assertListEqual(base_fields, list(ma.get_form(self.request).base_fields))

    def test_08_fields(self):
        ma = ModelAdmin(Inventory, self.site)
        fields = ['created_by', 'store', 'widget', 'quantity', 'deleted', 'link', 'ulink', 'dlink']
        self.assertListEqual(fields, list(ma.get_fields(self.request)))

    def test_09_field_lookup(self):
        ma = ModelAdmin(Inventory, self.site)
        self.assertTrue(ma.lookup_allowed('store', 'abc'))

    def test_10_exclude_list(self):
        user = User.objects.get(username=self.data['username'])
        s = Store.objects.create(name='whatever', location='New York', created_by=user)
        w = Widget.objects.create(name='whatever', created_by=user)
        i = Inventory.objects.create(store=s, widget=w, created_by=user)
        ma = ModelAdmin(Inventory, self.site)
        self.assertIsNone(ma.get_exclude(self.request, i))

class TestStoreAdmin(TestCase):
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

    def test_01_store_visible(self):
        url = '/admin/'
        user = User.objects.get(username=self.data['username'])
        response = self.c.get(path=url, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.csrf_cookie_set)
        self.assertTrue(self.c.login(**self.data))
        url = '/admin/simple/store/'
        response = self.c.get(path=url, headers=self.headers, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual('Select store to change | Django site admin', soup.title.string)
        self.assertIsNone(self.c.logout())

    def test_02_store_list_display(self):
        list_display = ('name', 'location', 'created_by')
        self.assertTupleEqual(list_display, StoreAdmin.list_display)

    def test_03_store_search_fields(self):
        search_fields = ('name', 'location')
        self.assertTupleEqual(search_fields, StoreAdmin.search_fields)

    def test_04_store_fields(self):
        fields = ('name', 'location', 'created_by')
        self.assertTupleEqual(fields, StoreAdmin.fields)

    def test_05_model_registered(self):
        ma = ModelAdmin(Store, self.site)
        self.assertEqual(str(ma), 'simple.ModelAdmin')
        
    def test_06_model_not_registered(self):
        self.assertFalse(self.site.is_registered(StoreAdmin))

    def test_07_base_fields(self):
        ma = ModelAdmin(Store, self.site)
        base_fields = ['created_by', 'name', 'location', 'deleted', 'link', 'ulink', 'dlink']
        self.assertListEqual(base_fields, list(ma.get_form(self.request).base_fields))

    def test_08_fields(self):
        ma = ModelAdmin(Store, self.site)
        fields = ['created_by', 'name', 'location', 'deleted', 'link', 'ulink', 'dlink']
        self.assertListEqual(fields, list(ma.get_fields(self.request)))

    def test_09_field_lookup(self):
        ma = ModelAdmin(Store, self.site)
        self.assertTrue(ma.lookup_allowed('name', 'abc'))

    def test_10_exclude_list(self):
        user = User.objects.get(username=self.data['username'])
        s = Store.objects.create(name='whatever', location='New York', created_by=user)
        ma = ModelAdmin(Store, self.site)
        self.assertIsNone(ma.get_exclude(self.request, s))

class TestWidgetAdmin(TestCase):
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

    def test_01_widget_visible(self):
        url = '/admin/'
        user = User.objects.get(username=self.data['username'])
        response = self.c.get(path=url, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.csrf_cookie_set)
        self.assertTrue(self.c.login(**self.data))
        url = '/admin/simple/widget/'
        response = self.c.get(path=url, headers=self.headers, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.reason_phrase)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual('Select widget to change | Django site admin', soup.title.string)
        self.assertIsNone(self.c.logout())

    def test_02_widget_list_display(self):
        list_display = ('name', 'sku', 'cost', 'created_by')
        self.assertTupleEqual(list_display, WidgetAdmin.list_display)

    def test_03_widget_search_fields(self):
        search_fields = ('name', 'sku', 'created_by')
        self.assertTupleEqual(search_fields, WidgetAdmin.search_fields)

    def test_04_widget_fields(self):
        fields = ('name', 'sku', 'cost', 'created_by')
        self.assertTupleEqual(fields, WidgetAdmin.fields)

    def test_05_model_registered(self):
        ma = ModelAdmin(Widget, self.site)
        self.assertEqual(str(ma), 'simple.ModelAdmin')
        
    def test_06_model_not_registered(self):
        self.assertFalse(self.site.is_registered(WidgetAdmin))

    def test_07_base_fields(self):
        ma = ModelAdmin(Widget, self.site)
        base_fields = ['created_by', 'name', 'sku', 'cost', 'deleted', 'link', 'ulink', 'dlink']
        self.assertListEqual(base_fields, list(ma.get_form(self.request).base_fields))

    def test_08_fields(self):
        ma = ModelAdmin(Widget, self.site)
        fields = ['created_by', 'name', 'sku', 'cost', 'deleted', 'link', 'ulink', 'dlink']
        self.assertListEqual(fields, list(ma.get_fields(self.request)))

    def test_09_field_lookup(self):
        ma = ModelAdmin(Widget, self.site)
        self.assertTrue(ma.lookup_allowed('name', 'abc'))

    def test_10_exclude_list(self):
        user = User.objects.get(username=self.data['username'])
        w = Widget.objects.create(name='whatever', created_by=user)
        ma = ModelAdmin(Widget, self.site)
        self.assertIsNone(ma.get_exclude(self.request, w))
