from decimal import Decimal

from django import forms

from complex.models import Event, Sensor

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['sensor', 'timestamp', 'location', 'status', 'camera',
                  'avg_temp', 'avg_pressure', 'pct_humidity', 'altitude',
                  'windspeed', 'deleted']

class SensorForm(forms.ModelForm):
    class Meta:
        model = Sensor
        fields = ['created_by', 'name', 'sku', 'serial_no', 'temp_units',
                  'pressure_units', 'alt_units', 'ws_units', 'climate',
                  'camera']
