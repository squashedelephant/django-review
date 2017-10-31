# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-31 21:23
from __future__ import unicode_literals

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('location', models.SmallIntegerField(choices=[(0, 'Nose'), (1, 'Cockpit'), (2, 'Fore Exit Door'), (3, 'Port Wing Tip'), (4, 'Port Wing'), (5, 'Starboard Wing Tip'), (6, 'Starboard Wing'), (7, 'Aft Exit Door'), (8, 'Tail')], default=1)),
                ('status', models.SmallIntegerField(choices=[(100, 'Online'), (101, 'Climate Fault'), (102, 'Camera Fault'), (103, 'Low Power')], default=100)),
                ('camera', models.SmallIntegerField(choices=[(200, 'N/A'), (201, 'Lens Obscured'), (202, 'Contrast Too High'), (203, 'Memory Full')], default=200)),
                ('avg_temp', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=5)),
                ('avg_pressure', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=5)),
                ('pct_humidity', models.PositiveIntegerField(default=0)),
                ('altitude', models.PositiveIntegerField(default=0)),
                ('windspeed', models.PositiveIntegerField(default=0)),
                ('deleted', models.BooleanField(default=False)),
                ('link', models.URLField(max_length=30, null=True)),
                ('ulink', models.URLField(max_length=30, null=True)),
                ('dlink', models.URLField(max_length=30, null=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('sku', models.CharField(max_length=20)),
                ('serial_no', models.CharField(max_length=20, unique=True)),
                ('temp_units', models.SmallIntegerField(choices=[(0, 'Fahrenheit'), (1, 'Celsius')], default=1)),
                ('pressure_units', models.SmallIntegerField(choices=[(2, 'psi'), (3, 'atm')], default=3)),
                ('alt_units', models.SmallIntegerField(choices=[(4, 'Miles'), (5, 'Kilometers')], default=5)),
                ('ws_units', models.SmallIntegerField(choices=[(6, 'Miles/Hour'), (7, 'Kilometers/Hour')], default=7)),
                ('installed', models.DateField(auto_now_add=True)),
                ('climate', models.BooleanField(default=True)),
                ('camera', models.BooleanField(default=False)),
                ('link', models.URLField(max_length=30, null=True)),
                ('ulink', models.URLField(max_length=30, null=True)),
                ('dlink', models.URLField(max_length=30, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='event',
            name='sensor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='complex.Sensor'),
        ),
    ]
