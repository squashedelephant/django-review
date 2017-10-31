from decimal import Decimal
from re import match

from django.forms import CharField, DecimalField, Form, ModelForm
from django.forms import NumberInput, TextInput, ValidationError

from simple.models import Inventory, Store, Widget

class InventoryForm(ModelForm):
    class Meta:
        model = Inventory
        fields = ['created_by', 'store', 'widget', 'quantity']

class StoreForm(ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'location']

class WidgetForm(Form):
    name = CharField(max_length=20,
                           required=True,
                           widget=TextInput)
    sku = CharField(max_length=10,
                          required=True,
                          widget=TextInput)
    cost = DecimalField(required=False,
                              max_value=9999.99,
                              min_value=0.00,
                              max_digits=6,
                              decimal_places=2,
                              widget=NumberInput)

    def clean_sku(self):
        invalid_fmt_msg = 'missing expected format: 111-111-11'
        sku = self.cleaned_data['sku']
        expected_format = '^(\d{3})-(\d{3})-(\d{2})$'
        if not match(expected_format, sku):
            raise ValidationError(invalid_fmt_msg)
        return sku
