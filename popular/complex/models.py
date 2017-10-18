# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

class Sensor(models.Model):
    ALTITUDE_UNITS = (
        (MILES, 'Miles')
        (KILOMETERS, 'Kilometers')
    )
    WINDSPEED_UNITS = (
        (MILES_PER_HOUR, 'Miles/Hour')
        (KILOMETERS_PER_HOUR, 'Kilometers/Hour')
    )
    created_by = models.ForeignKey(User,
                                   on_delete=models.CASCADE)
    name = models.CharField(max_length=20,
                            null=False,
                            blank=False,
                            unique=False)
    sku = models.CharField(max_length=20,
                           null=False,
                           blank=False,
                           unique=False)
    serial_no = models.CharField(max_length=20,
                                 null=False,
                                 blank=False,
                                 unique=True)
    alt_units = models.SmallIntegerField(choices=ALTITUDE_UNITS,
                                         default=KILOMETERS)
    ws_units = models.SmallIntegerField(choices=WINDSPEED_UNITS,
                                         default=KILOMETERS_PER_HOUR)
    installed = models.DateField(auto_now_add=True)
    climate = models.BooleanField(default=True)
    camera = models.BooleanField(default=False)
    link = models.URLField(max_length=30,
                           null=True,
                           blank=False)
    ulink = models.URLField(max_length=30,
                            null=True,
                            blank=False)
    dlink = models.URLField(max_length=30,
                            null=True,
                            blank=False)

    def __str__(self):
        return '{}_{}'.format(self.name, self.serial_no)

    def __repr__(self):
        return '{}_{}'.format(self.name, self.serial_no)

    def save(self, *args, **kwargs):
        super(Sensor, self).save(*args, **kwargs)
        kwargs = {'link': reverse('complex:sensor-detail',
                                  kwargs = {'pk': self.pk}),
                  'ulink': reverse('complex:sensor-update',
                                   kwargs = {'pk': self.pk}),
                  'dlink': reverse('complex:sensor-delete',
                                   kwargs = {'pk': self.pk})}
        Sensor.objects.filter(pk=self.pk).update(**kwargs)

class Event(models.Model):
    LOCATIONS = (
        (NOSE, 'Nose'),
        (COCKPIT, 'Cockpit'),
        (FORE_DOOR, 'Fore Exit Door'),
        (PORT_WING_TIP, 'Port Wing Tip'),
        (PORT_WING, 'Port Wing'),
        (STARBOARD_WING_TIP, 'Starboard Wing Tip'),
        (STARBOARD_WING, 'Starboard Wing'),
        (AFT_DOOR, 'Aft Exit Door'),
        (TAIL, 'Tail')
    )
    STATUS = (
        (ONLINE, 'Online'),
        (CLIMATE_FAULT, 'Climate Fault'),
        (CAMERA_FAULT, 'Camera Fault')
        (POWER, 'Low Power')
    )
    CAMERA = (
        (LENS, 'Lens Obscured'),
        (GLARE, 'Contrast Too High'),
        (MEMORY, 'Memory Full')
    )
    sensor = models.ForeignKey(Sensor)
    timestamp = models.DateTimeField() 
    location = models.SmallIntegerField(choices=LOCATIONS,
                                        default=COCKPIT)
    status = models.SmallIntegerField(choices=STATUS,
                                      default=ONLINE)
    camera = models.SmallIntegerField(choices=CAMERA,
                                       null=False,
                                       blank=False)
    avg_temp = models.DecimalField(max_digits=5,
                                   decimal_places=2,
                                   default=Decimal('0.00'))
    avg_pressure = models.DecimalField(max_digits=5,
                                       decimal_places=2,
                                       default=Decimal('0.00'))
    avg_humidity = models.PositiveIntegerField(max_length=100,
                                               default=0)
    altitude = models.DecimalField(max_digits=10,
                                   decimal_places=2,
                                   default=Decimal('0.00'))
    windspeed = models.DecimalField(max_digits=6,
                                    decimal_places=2,
                                    default=Decimal('0.00'))
    link = models.URLField(max_length=30,
                           null=True,
                           blank=False)
    ulink = models.URLField(max_length=30,
                            null=True,
                            blank=False)
    dlink = models.URLField(max_length=30,
                            null=True,
                            blank=False)

    def __str__(self):
        return '{}:{}'.format(self.sensor, self.id)

    def __repr__(self):
        return '{}_{}'.format(self.sensor, self.id)

    def save(self, *args, **kwargs):
        super(Event, self).save(*args, **kwargs)
        kwargs = {'link': reverse('complex:event-detail',
                                  kwargs = {'pk': self.pk}),
                  'ulink': reverse('complex:event-update',
                                   kwargs = {'pk': self.pk}),
                  'dlink': reverse('complex:event-delete',
                                   kwargs = {'pk': self.pk})}
        Event.objects.filter(pk=self.pk).update(**kwargs)

