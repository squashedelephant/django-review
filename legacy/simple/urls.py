from django.conf.urls import url
from django.contrib import admin

from simple.views import created, widget_create
from simple.views import widget_aggr, widget_delete, widget_detail
from simple.views import widget_list, widget_update
from simple.views import deleted, home, updated

app_name = 'simple'
urlpatterns = [
    url('^$',
        home,
        name='home'),
    url(r'^admin/',
        admin.site.urls,
        name='admin'), 
    url(r'^created/(?P<pk>\d+)/$',
        created,
        name='created'),
    url(r'^deleted/(?P<pk>\d+)/$',
        deleted,
        name='deleted'),
    url(r'^updated/(?P<pk>\d+)/$',
        updated,
        name='updated'),
    url(r'^widgets/create/$',
        widget_create,
        name='widget-create'),
    url(r'^widget/delete/(?P<pk>\d+)/$',
        widget_delete,
        name='widget-delete'),
    url(r'^widgets/(?P<pk>\d+)/$',
        widget_detail,
        name='widget-detail'),
    url(r'^widgets/$',
        widget_list,
        name='widget-list'),
    url(r'^widgets/page/(?P<page>\d+)/$',
        widget_list,
        name='widget-list'),
    url(r'^widgets/update/(?P<pk>\d+)/$',
        widget_update,
        name='widget-update'),
    url(r'^widgets/aggr/$',
        widget_aggr,
        name='widget-aggr'),
]
