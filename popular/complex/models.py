# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

class Device(models.Model):
    created_by = models.ForeignKey(User,
                                   on_delete=models.CASCADE)
    name = models.CharField(max_length=20,
                            null=False,
                            blank=False,
                            unique=True)
    sku = models.CharField(max_length=20,
                            null=False,
                            blank=False,
                            unique=True)
    night_vision = models.BooleanField(default=False)
    weather = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        if self.id:
            return '%s_%r' % (self.name, self.id)
        else:
            return '%r' % (self.name)

class Meter(models.Model):
    created_by = models.ForeignKey(User,
                                   on_delete=models.CASCADE)
    device = models.ForeignKey(Device,
                               blank=True,
                               null=True,
                               on_delete=models.CASCADE)
    location = models.CharField(max_length=20,
                                null=False,
                                blank=False,
                                unique=True)
    installed = models.DateField(auto_now_add=True)
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
        super(Meter, self).save(*args, **kwargs)
        kwargs = {'link': reverse('complex:meter-detail',
                                  kwargs = {'pk': self.pk}),
                  'ulink': reverse('complex:meter-update',
                                   kwargs = {'pk': self.pk}),
                  'dlink': reverse('complex:meter-delete',
                                   kwargs = {'pk': self.pk})}
        Meter.objects.filter(pk=self.pk).update(**kwargs)

    def __str__(self):
        return self.name

    def __repr__(self):
        if self.id:
            return '{0}_{1}:{2}' % (self.name, self.model, self.id)
        else:
            return '{0}_{1}' % (self.name, self.model)
