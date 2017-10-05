from django.contrib import admin

from simple.models import Inventory, Store, Widget

admin.site.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('store', 'widget', 'quantity', 'created_by')
    search_fields = ('store', 'widget')
    fields = ('store', 'widget', 'quantity', 'created_by')

admin.site.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'created_by')
    search_fields = ('name', 'location')
    fields = ('name', 'location', 'created_by')

admin.site.register(Widget)
class WidgetAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'cost', 'created_by')
    search_fields = ('name', 'sku', 'created_by')
    fields = ('name', 'sku', 'cost', 'created_by')
