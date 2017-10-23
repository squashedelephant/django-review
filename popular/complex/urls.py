from django.conf.urls import url
from django.contrib import admin

from complex.views import HomePageView, SensorCreateView
from complex.views import SensorDeleteView, SensorDetailView
from complex.views import SensorListView, SensorUpdateView

app_name = 'complex'
urlpatterns = [
    url('^$',
        HomePageView.as_view(),
        name='home'),
    url(r'^admin/',
        admin.site.urls,
        name='admin'),
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

