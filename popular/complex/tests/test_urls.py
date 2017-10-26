from django.core.urlresolvers import reverse, reverse_lazy
from django.test import TestCase

class TestGenericURLPath(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_01_index(self):
        expected = '/complex/'
        self.assertEqual(expected, reverse('complex:home'))
        self.assertEqual(expected, reverse_lazy('complex:home'))

    def test_02_thanks(self):
        expected = '/complex/thanks/'
        self.assertEqual(expected, reverse('complex:thanks'))
        self.assertEqual(expected, reverse_lazy('complex:thanks'))

class TestSensorURLPath(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_01_create(self):
        expected = '/complex/sensors/create/'
        self.assertEqual(expected, reverse('complex:sensor-create'))
        self.assertEqual(expected, reverse_lazy('complex:sensor-create'))

    def test_02_delete(self):
        expected = '/complex/sensors/1/delete/'
        self.assertEqual(expected, reverse('complex:sensor-delete',
                                           kwargs={'pk': 1}))
        self.assertEqual(expected, reverse_lazy('complex:sensor-delete',
                                                kwargs={'pk': 1}))

    def test_03_detail(self):
        expected = '/complex/sensors/1/'
        self.assertEqual(expected, reverse('complex:sensor-detail',
                                           kwargs={'pk': 1}))
        self.assertEqual(expected, reverse_lazy('complex:sensor-detail',
                                                kwargs={'pk': 1}))

    def test_04_list(self):
        expected = '/complex/sensors/'
        self.assertEqual(expected, reverse('complex:sensor-list'))
        self.assertEqual(expected, reverse_lazy('complex:sensor-list'))

    def test_05_full_update(self):
        expected = '/complex/sensors/1/update/'
        self.assertEqual(expected, reverse('complex:sensor-update',
                                           kwargs={'pk': 1}))
        self.assertEqual(expected, reverse_lazy('complex:sensor-update',
                                                kwargs={'pk': 1}))

    def test_06_paginate(self):
        expected = '/complex/sensors/%3Fpage=1'
        self.assertEqual(expected, reverse('complex:sensor-list',
                                           kwargs={'page': 1}))
        self.assertEqual(expected, reverse_lazy('complex:sensor-list',
                                                kwargs={'page': 1}))
        expected = '/complex/sensors/%3Fpage=2'
        self.assertEqual(expected, reverse('complex:sensor-list',
                                           kwargs={'page': 2}))
        self.assertEqual(expected, reverse_lazy('complex:sensor-list',
                                                kwargs={'page': 2}))

