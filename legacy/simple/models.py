# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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
    cost = models.FloatField(default=10.00,
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
