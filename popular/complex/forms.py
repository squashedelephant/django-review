from django.forms import ModelForm

from complex.models import Device, Meter

class DeviceForm(ModelForm):
    class Meta:
        model = Device
        fields = ['created_by', 'name', 'sku', 'night_vision', 'weather']

class MeterForm(ModelForm):
    class Meta:
        model = Meter
        fields = ['created_by', 'device', 'location', 'deleted']
