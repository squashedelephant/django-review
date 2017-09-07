# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from bs4 import BeautifulSoup
from json import dumps

from django.contrib.admin.sites import AdminSite
from django.contrib.admin.options import ModelAdmin
from django.contrib.auth.models import User
from django.test import Client, TestCase

from simple.admin import WidgetAdmin
from simple.models import Widget

class MockRequest:
    pass

class MockSuperUser:
    def has_perm(self, perm):
        return True

class TestSimpleAdmin(TestCase):
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
        self.ma = ModelAdmin(Widget, self.site)

    def tearDown(self):
        self.data = {}
        self.headers = {}
        self.c = None
        self.site = None
        self.request = None
        self.ma = None

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
        list_display = ('name', 'cost', 'created_by', 'link', 'ulink', 'dlink')
        self.assertTupleEqual(list_display, WidgetAdmin.list_display)

    def test_03_widget_search_fields(self):
        search_fields = (u'name', u'created_by', u'link', u'ulink', u'dlink')
        self.assertTupleEqual(search_fields, WidgetAdmin.search_fields)

    def test_04_widget_fields(self):
        fields = ('name', 'cost', 'created_by', 'link', 'ulink', 'dlink')
        self.assertTupleEqual(fields, WidgetAdmin.fields)

    def test_05_model_registered(self):
        self.assertEqual(str(self.ma), 'simple.ModelAdmin')
        
    def test_06_model_registered(self):
        self.assertFalse(self.site.is_registered(WidgetAdmin))

    def test_07_base_fields(self):
        base_fields = ['created_by', 'name', 'cost', 'deleted', 'link', 'ulink', 'dlink']
        self.assertListEqual(base_fields, list(self.ma.get_form(self.request).base_fields))

    def test_08_fields(self):
        fields = ['created_by', 'name', 'cost', 'deleted', 'link', 'ulink', 'dlink']
        self.assertListEqual(fields, list(self.ma.get_fields(self.request)))

    def test_09_field_lookup(self):
        self.assertTrue(self.ma.lookup_allowed('name', 'abc'))

    def test_10_exclude_list(self):
        user = User.objects.get(username=self.data['username'])
        w = Widget.objects.create(name='whatever', created_by=user)
        self.assertIsNone(self.ma.get_exclude(self.request, w))
