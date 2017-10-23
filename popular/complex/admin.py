# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from complex.models import Event, Sensor 

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'name', 'sku', 'serial_no', 'temp_units',
                    'pressure_units', 'alt_units', 'ws_units', 'installed',
                    'climate', 'camera')
    list_filter = ('name', 'sku', 'installed')
    search_fields = ('created_by', 'name', 'sku', 'serial_no', 'installed')
    fields = ('created_by', 'name', 'sku', 'serial_no', 'temp_units',
              'pressure_units', 'alt_units', 'ws_units', 'climate', 'camera')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('sensor', 'timestamp', 'location', 'status',
                    'camera', 'avg_temp', 'avg_pressure', 'pct_humidity',
                    'altitude', 'windspeed')
    list_filter = ('sensor', 'location')
    search_fields = ('sensor', 'timestamp', 'location', 'status')
    date_hierarchy = 'timestamp'
    ordering = ('-timestamp',)
    fields = ('sensor', 'timestamp', 'location', 'status', 'camera',
              'avg_temp', 'avg_pressure', 'pct_humidity', 'altitude',
              'windspeed')
