# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from complex.models import Device, Meter

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'night_vision', 'weather', 'created_by')
    list_filter = ('name', 'sku')
    search_fields = ('name', 'sku', 'created_by')
    fields = ('name', 'sku', 'night_vision', 'weather', 'created_by')

@admin.register(Meter)
class MeterAdmin(admin.ModelAdmin):
    list_display = ('device', 'location', 'installed', 'created_by',
                    'link', 'ulink', 'dlink')
    list_filter = ('device', 'created_by')
    search_fields = ('device', 'location', 'installed', 'created_by')
    date_hierarchy = 'installed'
    ordering = ('-installed',)
    fields = ('device', 'location', 'installed', 'created_by', 'deleted')
