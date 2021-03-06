from django.conf.urls import url
from django.contrib import admin

from complex.views import CreatedView, DeletedView, UpdatedView
from complex.views import EventCreateView, EventDeleteView
from complex.views import EventDetailView, EventListView
from complex.views import EventUpdateView, HomePageView
from complex.views import SensorCreateView, SensorDeleteView
from complex.views import SensorDetailView, SensorListView
from complex.views import SensorUpdateView, ThanksView

app_name = 'complex'
urlpatterns = [
    url('^$',
        HomePageView.as_view(),
        name='home'),
    url(r'^created/(?P<pk>\d+)/$',
        CreatedView.as_view(),
        name='created'),
    url(r'^deleted/(?P<pk>\d+)/$',
        DeletedView.as_view(),
        name='deleted'),
    url(r'^updated/(?P<pk>\d+)/$',
        UpdatedView.as_view(),
        name='updated'),
    url(r'^admin/',
        admin.site.urls,
        name='admin'),
    url(r'^events/add/$',
        EventCreateView.as_view(),
        name='event-create'),
    url(r'^events/(?P<pk>\d+)/delete/$',
        EventDeleteView.as_view(),
        name='event-delete'),
    url(r'^events/(?P<pk>\d+)/$',
        EventDetailView.as_view(),
        name='event-detail'),
    url(r'^events/$',
        EventListView.as_view(),
        name='event-list'),
    url(r'^events/\?page=(?P<page>\d+)$',
        EventListView.as_view(),
        name='event-list'),
    url(r'^events/(?P<pk>\d+)/update/$',
        EventUpdateView.as_view(),
        name='event-update'),
    url(r'^sensors/add/$',
        SensorCreateView.as_view(),
        name='sensor-create'),
    url(r'^sensors/(?P<pk>\d+)/delete/$',
        SensorDeleteView.as_view(),
        name='sensor-delete'),
    url(r'^sensors/(?P<pk>\d+)/$',
        SensorDetailView.as_view(),
        name='sensor-detail'),
    url(r'^sensors/$',
        SensorListView.as_view(),
        name='sensor-list'),
    url(r'^sensors/\?page=(?P<page>\d+)$',
        SensorListView.as_view(),
        name='sensor-list'),
    url(r'^sensors/(?P<pk>\d+)/update/$',
        SensorUpdateView.as_view(),
        name='sensor-update'),
    url(r'^thanks/(?P<pk>\d+)/$',
        ThanksView.as_view(),
        name='thanks'),
    url(r'^thanks/$',
        ThanksView.as_view(),
        name='thanks'),
]
