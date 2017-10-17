from django.conf.urls import url
from django.contrib import admin

from complex.views import home

app_name = 'complex'
urlpatterns = [
    url('^$',
        home,
        name='home'),
    url(r'^admin/',
        admin.site.urls,
        name='admin'),
]
