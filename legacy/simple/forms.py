from django import forms

from simple.models import Widget

class WidgetForm(forms.Form):
    name = forms.CharField(max_length=20,
                           required=True,
                           widget=forms.TextInput)
    cost = forms.FloatField(required=True,
                           widget=forms.TextInput)

    def __str__(self):
        return ' '.join(self.fields)

    def __repr__(self):
        return '%r.%r' % (self.__class__, '_'.join(self.fields))
