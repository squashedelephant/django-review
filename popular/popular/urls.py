from django.conf.urls import include, url
from django.contrib import admin

from django.contrib.auth.views import login, logout

from .views import main_page, user_page

urlpatterns = [
    url(r'^$', main_page),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', login),
    url(r'^logout/$', logout),
    url(r'^complex/', include('complex.urls')),
    url(r'^user/(\w+)/$', user_page),
]
