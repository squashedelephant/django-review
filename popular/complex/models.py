# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

class Sensor(models.Model):
    FAHRENHEIT = 0
    CELSIUS = 1

    TEMPERATURE_UNITS = (
        (FAHRENHEIT, 'Fahrenheit'),
        (CELSIUS, 'Celsius')
    )

    PSI = 2
    ATM = 3

    PRESSURE_UNITS = (
        (PSI, 'psi'),
        (ATM, 'atm')
    )

    MILES = 4
    KILOMETERS = 5

    ALTITUDE_UNITS = (
        (MILES, 'Miles'),
        (KILOMETERS, 'Kilometers')
    )

    MILES_PER_HOUR = 6
    KILOMETERS_PER_HOUR = 7

    WINDSPEED_UNITS = (
        (MILES_PER_HOUR, 'Miles/Hour'),
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
    temp_units = models.SmallIntegerField(choices=TEMPERATURE_UNITS,
                                          default=CELSIUS)
    pressure_units = models.SmallIntegerField(choices=PRESSURE_UNITS,
                                              default=ATM)
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
        return '{0}:{1}'.format(self.name, self.serial_no)

    def __repr__(self):
        if self.id:
            return '%r:%r' % (self.__class__, self.id)
        else:
            return '%r' % (self.__class__)

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
    NOSE = 0
    COCKPIT = 1
    FORE_DOOR = 2
    PORT_WING_TIP = 3
    PORT_WING = 4
    STARBOARD_WING_TIP = 5
    STARBOARD_WING = 6
    AFT_DOOR = 7
    TAIL = 8

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

    ONLINE = 100
    CLIMATE_FAULT = 101
    CAMERA_FAULT = 102
    LOW_POWER = 103

    STATUS = (
        (ONLINE, 'Online'),
        (CLIMATE_FAULT, 'Climate Fault'),
        (CAMERA_FAULT, 'Camera Fault'),
        (LOW_POWER, 'Low Power')
    )

    LENS = 200
    GLARE = 201
    MEMORY_FULL = 202

    CAMERA = (
        (LENS, 'Lens Obscured'),
        (GLARE, 'Contrast Too High'),
        (MEMORY_FULL, 'Memory Full')
    )
    sensor = models.ForeignKey(Sensor)
    timestamp = models.DateTimeField() 
    location = models.SmallIntegerField(choices=LOCATIONS,
                                        default=COCKPIT)
    status = models.SmallIntegerField(choices=STATUS,
                                      default=ONLINE)
    camera = models.SmallIntegerField(choices=CAMERA,
                                       null=True,
                                       blank=True)
    avg_temp = models.DecimalField(max_digits=5,
                                   decimal_places=2,
                                   default=Decimal('0.00'))
    avg_pressure = models.DecimalField(max_digits=5,
                                       decimal_places=2,
                                       default=Decimal('0.00'))
    pct_humidity = models.PositiveIntegerField(default=0)
    altitude = models.PositiveIntegerField(default=0)
    windspeed = models.PositiveIntegerField(default=0)
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

