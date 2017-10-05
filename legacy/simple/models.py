# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

class Widget(models.Model):
    created_by = models.ForeignKey(User,
                                   on_delete=models.CASCADE)
    name = models.CharField(max_length=20,
                            null=False,
                            blank=False,
                            unique=True)
    sku = models.CharField(max_length=10,
                           null=False,
                           blank=False,
                           unique=True)
    cost = models.DecimalField(max_digits=6,
                               decimal_places=2,
                               default=Decimal('0.00'))
    deleted = models.BooleanField(default=False)
    link = models.URLField(max_length=30,
                           null=True,
                           blank=False)
    ulink = models.URLField(max_length=30,
                            null=True,
                            blank=False)
    dlink = models.URLField(max_length=30,
                            null=True,
                            blank=False)

    def save(self, *args, **kwargs):
        super(Widget, self).save(*args, **kwargs)
        kwargs = {'link': reverse('simple:widget-detail',
                                  kwargs = {'pk': self.pk}),
                  'ulink': reverse('simple:widget-update',
                                   kwargs = {'pk': self.pk}),
                  'dlink': reverse('simple:widget-delete',
                                   kwargs = {'pk': self.pk})}
        Widget.objects.filter(pk=self.pk).update(**kwargs)

    def __str__(self):
        return self.name

    def __repr__(self):
        if self.id:
            return '%r:%r' % (self.__class__, self.id)
        else:
            return '%r' % (self.__class__)

class Store(models.Model):
    created_by = models.ForeignKey(User,
                                   on_delete=models.CASCADE)
    name = models.CharField(max_length=20,
                            null=False,
                            blank=False,
                            unique=True)
    location = models.CharField(max_length=20,
                                null=False,
                                blank=False,
                                unique=True)
    deleted = models.BooleanField(default=False)
    link = models.URLField(max_length=30,
                           null=True,
                           blank=False)
    ulink = models.URLField(max_length=30,
                            null=True,
                            blank=False)
    dlink = models.URLField(max_length=30,
                            null=True,
                            blank=False)

    def save(self, *args, **kwargs):
        super(Store, self).save(*args, **kwargs)
        kwargs = {'link': reverse('simple:store-detail',
                                  kwargs = {'pk': self.pk}),
                  'ulink': reverse('simple:store-update',
                                   kwargs = {'pk': self.pk}),
                  'dlink': reverse('simple:store-delete',
                                   kwargs = {'pk': self.pk})}
        Store.objects.filter(pk=self.pk).update(**kwargs)

    def __str__(self):
        return '{0}:{1}'.format(self.name, self.location)

    def __repr__(self):
        if self.id:
            return '%r:%r' % (self.__class__, self.id)
        else:
            return '%r' % (self.__class__)

class Inventory(models.Model):
    created_by = models.ForeignKey(User,
                                   null=False,
                                   on_delete=models.CASCADE)
    store = models.ForeignKey(Store,
                              null=False,
                              on_delete=models.CASCADE)
    widget = models.ForeignKey(Widget,
                               null=True,
                               on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0,
                                           null=False,
                                           blank=False)
    deleted = models.BooleanField(default=False)
    link = models.URLField(max_length=30,
                           null=True,
                           blank=False)
    ulink = models.URLField(max_length=30,
                            null=True,
                            blank=False)
    dlink = models.URLField(max_length=30,
                            null=True,
                            blank=False)

    def save(self, *args, **kwargs):
        super(Inventory, self).save(*args, **kwargs)
        kwargs = {'link': reverse('simple:inventory-detail',
                                  kwargs = {'pk': self.pk}),
                  'ulink': reverse('simple:inventory-update',
                                   kwargs = {'pk': self.pk}),
                  'dlink': reverse('simple:inventory-delete',
                                   kwargs = {'pk': self.pk})}
        Inventory.objects.filter(pk=self.pk).update(**kwargs)

    def __str__(self):
        return '{0}:{1}'.format(self.store, self.widget)

    def __repr__(self):
        if self.id:
            return '%r:%r' % (self.__class__, self.id)
        else:
            return '%r' % (self.__class__)
