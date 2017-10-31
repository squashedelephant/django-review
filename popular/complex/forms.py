from decimal import Decimal
from re import match

from django.forms import CharField, ModelForm, ValidationError
from django.utils.timezone import datetime

from complex.models import Event, Sensor

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['sensor', 'timestamp', 'location', 'status', 'camera',
                  'avg_temp', 'avg_pressure', 'pct_humidity', 'altitude',
                  'windspeed']

class SensorForm(ModelForm):
    class Meta:
        model = Sensor
        fields = ['created_by', 'name', 'sku', 'serial_no', 'temp_units',
                  'pressure_units', 'alt_units', 'ws_units', 'climate',
                  'camera']

    def clean_sku(self):
        invalid_fmt_msg = 'missing expected format: 111-11111-111'
        sku = self.cleaned_data['sku']
        expected_format = '^(\d{3})-(\d{5})-(\d{3})$'
        if not match(expected_format, sku):
            raise ValidationError(invalid_fmt_msg)
        return sku

    def clean_serial_no(self):
        duplicate_msg = 'serial_no already exists'
        serial_no = self.cleaned_data['serial_no']
        try:
            Sensor.objects.get(serial_no=serial_no.upper())
            print('also failed in clean_serial_no')
            raise ValidationError(duplicate_msg)
        except Sensor.DoesNotExist as e:
            return serial_no.upper()

class SensorUpdateForm(SensorForm):
    serial_no = CharField(disabled=True)

    def clean_serial_no(self):
        serial_no = self.cleaned_data['serial_no']
        return serial_no.upper()
