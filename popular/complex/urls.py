from django.conf.urls import url
from django.contrib import admin

from complex.views import EventCreateView, EventDeleteView
from complex.views import EventDetailView, EventListView
from complex.views import EventUpdateView, HomePageView

from complex.views import SensorCreateView, SensorDeleteView
from complex.views import SensorDetailView, SensorListView
from complex.views import SensorUpdateView

app_name = 'complex'
urlpatterns = [
    url('^$',
        HomePageView.as_view(),
        name='home'),
    url(r'^admin/',
        admin.site.urls,
        name='admin'),
    url(r'^event/create/$',
        EventCreateView.as_view(),
        name='event-create'),
    url(r'^event/delete/(?P<pk>\d+)/$',
        EventDeleteView.as_view(),
        name='event-delete'),
    url(r'^event/(?P<pk>\d+)/$',
        EventDetailView.as_view(),
        name='event-detail'),
    url(r'^events/$',
        EventListView.as_view(),
        name='event-list'),
    url(r'^events/page/(?P<page>\d+)/$',
        EventListView.as_view(),
        name='event-list'),
    url(r'^event/update/(?P<pk>\d+)/$',
        EventUpdateView.as_view(),
        name='event-update'),
    url(r'^sensor/create/$',
        SensorCreateView.as_view(),
        name='sensor-create'),
    url(r'^sensor/delete/(?P<pk>\d+)/$',
        SensorDeleteView.as_view(),
        name='sensor-delete'),
    url(r'^sensor/(?P<pk>\d+)/$',
        SensorDetailView.as_view(),
        name='sensor-detail'),
    url(r'^sensors/$',
        SensorListView.as_view(),
        name='sensor-list'),
    url(r'^sensors/page/(?P<page>\d+)/$',
        SensorListView.as_view(),
        name='sensor-list'),
    url(r'^sensor/update/(?P<pk>\d+)/$',
        SensorUpdateView.as_view(),
        name='sensor-update')
]

