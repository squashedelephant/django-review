# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.test import TestCase
from django.db import IntegrityError

from simple.models import Inventory, Store, Widget
from simple.tests.utils import get_locations, get_random_sku, get_random_cost

class TestInventoryModel(TestCase):
    def setUp(self):
        user = User.objects.get(username='qa')
        self.locations = get_locations()
        self.i_data = {'quantity': 1,
                       'created_by': user,
                       'deleted': False}
        self.s_data = {'name': 'Moon',
                       'location': self.locations[0],
                       'created_by': user,
                       'deleted': False}
        self.w_data = {'name': 'Moon',
                       'sku': get_random_sku(),
                       'cost': get_random_cost(),
                       'created_by': user,
                       'deleted': False}

    def tearDown(self):
        self.i_data = None
        self.s_data = None
        self.w_data = None

    def test_01_object(self):
        i = Inventory()
        self.assertEqual("<class 'simple.models.Inventory'>", repr(i))
        s = Store.objects.create(**self.s_data)
        w = Widget.objects.create(**self.w_data)
        self.i_data.update({'store': s,
                            'widget': w})
        i = Inventory.objects.create(**self.i_data)
        self.assertEqual('{0}:{1}'.format(self.i_data['store'],
                                          self.i_data['widget']),
                         str(i))
        self.assertEqual("<class 'simple.models.Inventory'>:{}".format(i.id),
                                                                       repr(i))

    def test_02_create(self):
        s = Store.objects.create(**self.s_data)
        w = Widget.objects.create(**self.w_data)
        self.i_data.update({'store': s,
                            'widget': w})
        i = Inventory.objects.create(**self.i_data)
        self.assertEqual(1, i.id)

    def test_03_get(self):
        s = Store.objects.create(**self.s_data)
        w = Widget.objects.create(**self.w_data)
        self.i_data.update({'store': s,
                            'widget': w})
        expected = Inventory.objects.create(**self.i_data)
        actual = Inventory.objects.get(id=expected.id)
        self.assertEqual(expected.id, actual.id)

    def test_04_update(self):
        s = Store.objects.create(**self.s_data)
        w = Widget.objects.create(**self.w_data)
        self.i_data.update({'store': s,
                            'widget': w})
        expected = Inventory.objects.create(**self.i_data)
        new_quantity = 5
        expected.quantity = new_quantity
        expected.save()
        actual = Inventory.objects.get(id=expected.id)
        self.assertEqual(new_quantity, actual.quantity)

    def test_05_delete(self):
        s = Store.objects.create(**self.s_data)
        w = Widget.objects.create(**self.w_data)
        self.i_data.update({'store': s,
                            'widget': w})
        expected = Inventory.objects.create(**self.i_data)
        expected.delete()
        with self.assertRaises(Inventory.DoesNotExist) as context:
            Inventory.objects.get(pk=expected.id)
        msg = 'Inventory matching query does not exist'
        self.assertIn(msg, str(context.exception))
 
    def test_06_filter(self):
        quantities = [73, 53, 37]
        s = Store.objects.create(**self.s_data)
        w = Widget.objects.create(**self.w_data)
        for idx in range(len(quantities)):
            self.i_data.update({'quantity': quantities[idx],
                                'store': s,
                                'widget': w})
            Inventory.objects.create(**self.i_data)
        actual = Inventory.objects.filter(deleted=False) 
        self.assertEqual(len(quantities), len(actual))

    def test_07_save(self):
        s = Store.objects.create(**self.s_data)
        w = Widget.objects.create(**self.w_data)
        self.i_data.update({'store': s,
                            'widget': w})
        expected = Inventory(**self.i_data)
        expected.save()
        self.assertIsNone(expected.link)
        self.assertIsNone(expected.dlink)
        self.assertIsNone(expected.ulink)
        actual = Inventory.objects.get(id=expected.id)
        self.assertIsNotNone(actual.link)
        self.assertIsNotNone(actual.dlink)
        self.assertIsNotNone(actual.ulink)


class TestStoreModel(TestCase):
    def setUp(self):
        user = User.objects.get(username='qa')
        self.locations = get_locations()
        self.data= {'name': 'Moon',
                           'location': self.locations[0],
                           'created_by': user,
                           'deleted': False}

    def tearDown(self):
        self.data = None

    def test_01_object(self):
        s = Store()
        self.assertEqual("<class 'simple.models.Store'>", repr(s))
        s = Store.objects.create(**self.data)
        self.assertEqual('{0}:{1}'.format(self.data['name'],
                                          self.data['location']),
                         str(s))
        self.assertEqual("<class 'simple.models.Store'>:{}".format(s.id),
                                                                   repr(s))

    def test_02_create(self):
        s = Store.objects.create(**self.data)
        self.assertEqual(1, s.id)

    def test_03_get(self):
        expected = Store.objects.create(**self.data)
        actual = Store.objects.get(id=expected.id)
        self.assertEqual(expected.id, actual.id)

    def test_04_update(self):
        expected = Store.objects.create(**self.data)
        new_name = 'Sun'
        expected.name = new_name
        expected.save()
        actual = Store.objects.get(id=expected.id)
        self.assertEqual(new_name, actual.name)

    def test_05_delete(self):
        expected = Store.objects.create(**self.data)
        expected.delete()
        with self.assertRaises(Store.DoesNotExist) as context:
            Store.objects.get(pk=expected.id)
        msg = 'Store matching query does not exist'
        self.assertIn(msg, str(context.exception))
 
    def test_06_filter(self):
        names = ['Moon', 'Sun', 'Star']
        locations = ['El Segundo', 'Oakland', 'Richmond']
        for idx in range(len(names)):
            self.data.update({'name': names[idx],
                                    'location': locations[idx]})
            Store.objects.create(**self.data)
        actual = Store.objects.filter(deleted=False) 
        self.assertEqual(len(names), len(actual))

    def test_07_save(self):
        expected = Store(**self.data)
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
        self.data = {'name': 'Moon',
                     'sku': get_random_sku(),
                     'cost': get_random_cost(),
                     'created_by': user,
                     'deleted': False}

    def tearDown(self):
        self.data = None

    def test_01_object(self):
        w = Widget()
        self.assertEqual("<class 'simple.models.Widget'>", repr(w))
        w = Widget.objects.create(**self.data)
        self.assertEqual(self.data['name'], str(w))
        self.assertEqual("<class 'simple.models.Widget'>:{}".format(w.id),
                                                                    repr(w))

    def test_02_create(self):
        w = Widget.objects.create(**self.data)
        self.assertEqual(1, w.id)

    def test_03_get(self):
        expected = Widget.objects.create(**self.data)
        actual = Widget.objects.get(id=expected.id)
        self.assertEqual(expected.id, actual.id)

    def test_04_update(self):
        expected = Widget.objects.create(**self.data)
        new_name = 'Sun'
        expected.name = new_name
        expected.save()
        actual = Widget.objects.get(id=expected.id)
        self.assertEqual(new_name, actual.name)

    def test_05_delete(self):
        expected = Widget.objects.create(**self.data)
        expected.delete()
        with self.assertRaises(Widget.DoesNotExist) as context:
            Widget.objects.get(pk=expected.id)
        msg = 'Widget matching query does not exist'
        self.assertIn(msg, str(context.exception))
 
    def test_06_filter(self):
        names = ['Moon', 'Sun', 'Star']
        for idx in range(len(names)):
            self.data.update({'name': names[idx],
                                    'sku': get_random_sku()})
            Widget.objects.create(**self.data)
        actual = Widget.objects.filter(deleted=False) 
        self.assertEqual(len(names), len(actual))

    def test_07_save(self):
        expected = Widget(**self.data)
        expected.save()
        self.assertIsNone(expected.link)
        self.assertIsNone(expected.dlink)
        self.assertIsNone(expected.ulink)
        actual = Widget.objects.get(id=expected.id)
        self.assertIsNotNone(actual.link)
        self.assertIsNotNone(actual.dlink)
        self.assertIsNotNone(actual.ulink)
