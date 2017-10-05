from decimal import Decimal

from django import forms

from simple.models import Inventory, Store, Widget

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['created_by', 'store', 'widget', 'quantity']

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'location']

class WidgetForm(forms.Form):
    name = forms.CharField(max_length=20,
                           required=True,
                           widget=forms.TextInput)
    sku = forms.CharField(max_length=10,
                          required=True,
                          widget=forms.TextInput)
    cost = forms.DecimalField(required=False,
                              max_value=9999.99,
                              min_value=0.00,
                              max_digits=6,
                              decimal_places=2,
                              widget=forms.NumberInput)
