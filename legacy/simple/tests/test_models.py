# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.test import TestCase
from django.db import IntegrityError

from simple.models import Inventory, Store, Widget
from simple.tests.utils import get_locations, get_random_sku, get_random_cost

class TestStoreModel(TestCase):
    def setUp(self):
        user = User.objects.get(username='qa')
        self.locations = get_locations()
        self.data_valid = {'name': 'Moon',
                           'location': self.locations[0],
                           'created_by': user,
                           'deleted': False}

    def tearDown(self):
        self.data = None

    def test_01_object(self):
        s = Store()
        self.assertEqual("<class 'simple.models.Store'>", repr(s))
        s = Store.objects.create(**self.data_valid)
        self.assertEqual('{0}:{1}'.format(self.data_valid['name'],
                                          self.data_valid['location']),
                         str(s))
        self.assertEqual("<class 'simple.models.Store'>:{}".format(s.id),
                                                                   repr(s))

    def test_02_create(self):
        s = Store.objects.create(**self.data_valid)
        self.assertEqual(1, s.id)

    def test_03_get(self):
        expected = Store.objects.create(**self.data_valid)
        actual = Store.objects.get(id=expected.id)
        self.assertEqual(expected.id, actual.id)

    def test_04_update(self):
        expected = Store.objects.create(**self.data_valid)
        new_name = 'Sun'
        expected.name = new_name
        expected.save()
        actual = Store.objects.get(id=expected.id)
        self.assertEqual(new_name, actual.name)

    def test_05_delete(self):
        expected = Store.objects.create(**self.data_valid)
        expected.delete()
        with self.assertRaises(Store.DoesNotExist) as context:
            Store.objects.get(pk=expected.id)
        msg = 'Store matching query does not exist'
        self.assertIn(msg, str(context.exception))
 
    def test_06_filter(self):
        names = ['Moon', 'Sun', 'Star']
        locations = ['El Segundo', 'Oakland', 'Richmond']
        for idx in range(len(names)):
            self.data_valid.update({'name': names[idx],
                                    'location': locations[idx]})
            Store.objects.create(**self.data_valid)
        actual = Store.objects.filter(deleted=False) 
        self.assertEqual(len(names), len(actual))

    def test_07_save(self):
        expected = Store(**self.data_valid)
        expected.save()
        self.assertIsNone(expected.link)
        self.assertIsNone(expected.dlink)
        self.assertIsNone(expected.ulink)
        actual = Store.objects.get(id=expected.id)
        self.assertIsNotNone(actual.link)
        self.assertIsNotNone(actual.dlink)
        self.assertIsNotNone(actual.ulink)

class TestWidgetModel(TestCase):
    def setUp(self):
        user = User.objects.get(username='qa')
        self.data_valid = {'name': 'Moon',
                           'sku': get_random_sku(),
                           'cost': get_random_cost(),
                           'created_by': user,
                           'deleted': False}

    def tearDown(self):
        self.data = None

    def test_01_object(self):
        w = Widget()
        self.assertEqual("<class 'simple.models.Widget'>", repr(w))
        w = Widget.objects.create(**self.data_valid)
        self.assertEqual(self.data_valid['name'], str(w))
        self.assertEqual("<class 'simple.models.Widget'>:{}".format(w.id),
                                                                    repr(w))

    def test_02_create(self):
        w = Widget.objects.create(**self.data_valid)
        self.assertEqual(1, w.id)

    def test_03_get(self):
        expected = Widget.objects.create(**self.data_valid)
        actual = Widget.objects.get(id=expected.id)
        self.assertEqual(expected.id, actual.id)

    def test_04_update(self):
        expected = Widget.objects.create(**self.data_valid)
        new_name = 'Sun'
        expected.name = new_name
        expected.save()
        actual = Widget.objects.get(id=expected.id)
        self.assertEqual(new_name, actual.name)

    def test_05_delete(self):
        expected = Widget.objects.create(**self.data_valid)
        expected.delete()
        with self.assertRaises(Widget.DoesNotExist) as context:
            Widget.objects.get(pk=expected.id)
        msg = 'Widget matching query does not exist'
        self.assertIn(msg, str(context.exception))
 
    def ttest_06_filter(self):
        names = ['Moon', 'Sun', 'Star']
        for idx in range(len(names)):
            self.data_valid.update({'name': names[idx],
                                    'sku': get_random_sku()})
            Widget.objects.create(**self.data_valid)
        actual = Store.objects.filter(deleted=False) 
        self.assertEqual(len(names), len(actual))

    def test_07_save(self):
        expected = Widget(**self.data_valid)
        expected.save()
        self.assertIsNone(expected.link)
        self.assertIsNone(expected.dlink)
        self.assertIsNone(expected.ulink)
        actual = Widget.objects.get(id=expected.id)
        self.assertIsNotNone(actual.link)
        self.assertIsNotNone(actual.dlink)
        self.assertIsNotNone(actual.ulink)
