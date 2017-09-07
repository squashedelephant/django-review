from django.contrib import admin

from simple.models import Widget

admin.site.register(Widget)
class WidgetAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost', 'created_by', 'link', 'ulink', 'dlink')
    search_fields = ('name', 'created_by', 'link', 'ulink', 'dlink')
    fields = ('name', 'cost', 'created_by', 'link', 'ulink', 'dlink')
