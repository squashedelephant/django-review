# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal
from random import randint, random

from django.contrib.auth.models import User
from django.test import TestCase

from simple.forms import InventoryForm, StoreForm, WidgetForm
from simple.models import Store, Widget
from simple.tests.utils import get_random_cost, get_random_location
from simple.tests.utils import get_random_name, get_random_sku

class TestInventoryForm(TestCase):
    def setUp(self):
        value = randint(1000, 5000)
        self.user = User.objects.get(username='superuser')
        self.s_data = {'name': get_random_name(),
                       'location': get_random_location(),
                       'created_by': self.user}
        self.w_data = {'name': get_random_name(),
                       'sku': get_random_sku(),
                       'cost': get_random_cost(),
                       'created_by': self.user}
        self.data_valid = {'quantity': value,
                           'created_by': self.user.id}
        self.data_large = {'quantity': value * value,
                           'created_by': self.user.id}
        self.data_empty = {'quantity': None,
                           'created_by': self.user.id}
        self.data_blank = {'quantity': '',
                           'created_by': self.user.id}

    def tearDown(self):
        self.data_valid = None
        self.data_large = None
        self.data_empty = None
        self.data_blank = None

    def _create_store(self):
        try:
            store = Store.objects.create(**self.s_data)
            return store.id
        except Store.DoesNotExist:
            return None
        
    def _create_widget(self):
        try:
            widget = Widget.objects.create(**self.w_data)
            return widget.id
        except Widget.DoesNotExist:
            return None
        
    def test_01_quantity_valid(self):
        self.data_valid.update({'store': self._create_store(),
                                'widget': self._create_widget()})
        form = InventoryForm(data=self.data_valid)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.is_bound)
        self.assertEqual(self.data_valid['quantity'],
                         form.data['quantity'])

    def test_02_quantity_empty(self):
        self.data_empty.update({'store': self._create_store(),
                                'widget': self._create_widget()})
        form = InventoryForm(data=self.data_empty)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.is_bound)
        self.assertEqual(1, len(form.errors['quantity']))
        self.assertEqual(u'This field is required.',
                         form.errors['quantity'][0])

    def test_03_quantity_blank(self):
        self.data_blank.update({'store': self._create_store(),
                                'widget': self._create_widget()})
        form = InventoryForm(data=self.data_blank)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.is_bound)
        self.assertEqual(1, len(form.errors['quantity']))
        self.assertEqual(u'This field is required.',
                         form.errors['quantity'][0])

    def test_04_object(self):
        self.data_valid.update({'store': self._create_store(),
                                'widget': self._create_widget()})
        form = InventoryForm(data=self.data_valid)
        self.assertIn('store', str(form))
        self.assertIn('widget', str(form))
        self.assertEqual('<InventoryForm bound=True, valid=True, fields=(created_by;store;widget;quantity)>',
                         repr(form))

class TestStoreForm(TestCase):
    def setUp(self):
        value = randint(1000, 5000)
        self.data_valid = {'name': get_random_name(),
                           'location': get_random_location()}
        self.data_long = {'name': 'Exceedingly Long {}'.format(value),
                          'location': get_random_location()}
        self.data_empty = {'name': None,
                           'location': get_random_location()}
        self.data_blank = {'name': '',
                           'location': get_random_location()}

    def tearDown(self):
        self.data_valid = None
        self.data_long = None
        self.data_empty = None
        self.data_blank = None

    def test_01_name_valid(self):
        form = StoreForm(data=self.data_valid)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.is_bound)
        self.assertEqual(self.data_valid['name'],
                         form.data['name'])

    def test_02_name_too_long(self):
        form = StoreForm(data=self.data_long)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.is_bound)
        self.assertEqual(1, len(form.errors['name']))
        errmsg = u'Ensure this value has at most 20 characters (it has 21).'
        self.assertEqual(errmsg,
                         form.errors['name'][0])

    def test_03_name_empty(self):
        form = StoreForm(data=self.data_empty)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.is_bound)
        self.assertEqual(1, len(form.errors['name']))
        self.assertEqual(u'This field is required.',
                         form.errors['name'][0])

    def test_04_name_blank(self):
        form = StoreForm(data=self.data_blank)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.is_bound)
        self.assertEqual(1, len(form.errors['name']))
        self.assertEqual(u'This field is required.',
                         form.errors['name'][0])

    def test_05_object(self):
        form = StoreForm(data=self.data_valid)
        self.assertIn('name', str(form))
        self.assertEqual('<StoreForm bound=True, valid=True, fields=(name;location)>',
                         repr(form))

class TestWidgetForm(TestCase):
    def setUp(self):
        value = randint(1000, 5000)
        self.data_valid = {'name': get_random_name(),
                           'sku': get_random_sku(),
                           'cost': get_random_cost()}
        self.data_long = {'name': 'Exceedingly Long {}'.format(value),
                          'sku': get_random_sku(),
                          'cost': get_random_cost()}
        self.data_empty = {'name': None,
                           'sku': get_random_sku(),
                           'cost': get_random_cost()}
        self.data_blank = {'name': '',
                           'sku': get_random_sku(),
                           'cost': get_random_cost()}

    def tearDown(self):
        self.data_valid = None
        self.data_long = None
        self.data_empty = None
        self.data_blank = None

    def test_01_name_valid(self):
        form = WidgetForm(data=self.data_valid)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.is_bound)
        self.assertEqual(self.data_valid['name'],
                         form.data['name'])

    def test_02_name_too_long(self):
        form = WidgetForm(data=self.data_long)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.is_bound)
        self.assertEqual(1, len(form.errors['name']))
        errmsg = u'Ensure this value has at most 20 characters (it has 21).'
        self.assertEqual(errmsg,
                         form.errors['name'][0])

    def test_03_name_empty(self):
        form = WidgetForm(data=self.data_empty)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.is_bound)
        self.assertEqual(1, len(form.errors['name']))
        self.assertEqual(u'This field is required.',
                         form.errors['name'][0])

    def test_04_name_blank(self):
        form = WidgetForm(data=self.data_blank)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.is_bound)
        self.assertEqual(1, len(form.errors['name']))
        self.assertEqual(u'This field is required.',
                         form.errors['name'][0])

    def test_05_object(self):
        form = WidgetForm(data=self.data_valid)
        self.assertIn('name', str(form))
        self.assertEqual('<WidgetForm bound=True, valid=True, fields=(name;sku;cost)>',
                         repr(form))
