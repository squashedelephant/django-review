# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.test import TestCase

from simple.models import Widget

class TestSimpleModel(TestCase):
    def setUp(self):
        user = User.objects.get(username='qa')
        self.data_valid = {'name': 'Moon',
                           'created_by': user,
                           'deleted': False}

    def tearDown(self):
        self.data = None

    def test_01_object(self):
        w = Widget()
        self.assertEqual("<class 'simple.models.Widget'>", repr(w))
        w = Widget.objects.create(**self.data_valid)
        self.assertEqual(self.data_valid['name'], str(w))
        self.assertEqual("<class 'simple.models.Widget'>:{}".format(w.id), repr(w))

    def test_02_create(self):
        w = Widget.objects.create(**self.data_valid)
        self.assertEqual(1, w.id)

    def test_03_get(self):
        expected = Widget.objects.create(**self.data_valid)
        actual = Widget.objects.get(id=expected.id)
        self.assertEqual(expected.id, actual.id)

    def test_03_update(self):
        expected = Widget.objects.create(**self.data_valid)
        new_name = 'Sun'
        expected.name = new_name
        expected.save()
        actual = Widget.objects.get(id=expected.id)
        self.assertEqual(new_name, actual.name)

    def test_04_delete(self):
        expected = Widget.objects.create(**self.data_valid)
        expected.delete()
        with self.assertRaises(Widget.DoesNotExist) as context:
            Widget.objects.get(pk=expected.id)
        msg = 'Widget matching query does not exist'
        self.assertIn(msg, str(context.exception))
 
    def test_05_filter(self):
        names = ['Moon', 'Sun', 'Star']
        for name in names:
            self.data_valid.update({'name': name})
            Widget.objects.create(**self.data_valid)
        actual = Widget.objects.filter(deleted=False) 
        self.assertEqual(len(names), len(actual))

    def test_06_save(self):
        expected = Widget(**self.data_valid)
        expected.save()
        self.assertIsNone(expected.link)
        self.assertIsNone(expected.dlink)
        self.assertIsNone(expected.ulink)
        actual = Widget.objects.get(id=expected.id)
        self.assertIsNotNone(actual.link)
        self.assertIsNotNone(actual.dlink)
        self.assertIsNotNone(actual.ulink)
