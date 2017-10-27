from django.core.urlresolvers import reverse, reverse_lazy
from django.test import TestCase

class TestGenericURLConf(TestCase):
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

class TestEventURLConf(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_01_create(self):
        expected = '/complex/events/add/'
        self.assertEqual(expected, reverse('complex:event-create'))
        self.assertEqual(expected, reverse_lazy('complex:event-create'))

    def test_02_delete(self):
        expected = '/complex/events/1/delete/'
        self.assertEqual(expected, reverse('complex:event-delete',
                                           kwargs={'pk': 1}))
        self.assertEqual(expected, reverse_lazy('complex:event-delete',
                                                kwargs={'pk': 1}))

    def test_03_detail(self):
        expected = '/complex/events/1/'
        self.assertEqual(expected, reverse('complex:event-detail',
                                           kwargs={'pk': 1}))
        self.assertEqual(expected, reverse_lazy('complex:event-detail',
                                                kwargs={'pk': 1}))

    def test_04_list(self):
        expected = '/complex/events/'
        self.assertEqual(expected, reverse('complex:event-list'))
        self.assertEqual(expected, reverse_lazy('complex:event-list'))

    def test_05_full_update(self):
        expected = '/complex/events/1/update/'
        self.assertEqual(expected, reverse('complex:event-update',
                                           kwargs={'pk': 1}))
        self.assertEqual(expected, reverse_lazy('complex:event-update',
                                                kwargs={'pk': 1}))

    def test_06_paginate(self):
        expected = '/complex/events/%3Fpage=1'
        self.assertEqual(expected, reverse('complex:event-list',
                                           kwargs={'page': 1}))
        self.assertEqual(expected, reverse_lazy('complex:event-list',
                                                kwargs={'page': 1}))
        expected = '/complex/events/%3Fpage=2'
        self.assertEqual(expected, reverse('complex:event-list',
                                           kwargs={'page': 2}))
        self.assertEqual(expected, reverse_lazy('complex:event-list',
                                                kwargs={'page': 2}))


class TestSensorURLConf(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_01_create(self):
        expected = '/complex/sensors/add/'
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
