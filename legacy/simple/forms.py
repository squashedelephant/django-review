from decimal import Decimal

from django import forms

from simple.models import Widget

class WidgetForm(forms.Form):
    name = forms.CharField(max_length=20,
                           required=True,
                           widget=forms.TextInput)
    cost = forms.DecimalField(required=False,
                              max_value=9999.99,
                              min_value=0.00,
                              max_digits=6,
                              decimal_places=2,
                              widget=forms.NumberInput)

    def __str__(self):
        return ' '.join(self.fields)

    def __repr__(self):
        return '%r.%r' % (self.__class__, '_'.join(self.fields))
