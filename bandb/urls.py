from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.http import HttpResponse

admin.autodiscover()

from .views import *

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^the-hut$', HutView.as_view(), name='hut'),
    url(r'^bookings(?:/(?P<year>\d{4})/(?P<month>\d{2}))?$', RatesView.as_view(), name='rates'),
    url(r'^find-us$', AreaView.as_view(), name='area'),
    url(r'^things-to-know$', ThingsToKnowView.as_view(), name='things_to_know'),

    url(r'^admin/', include(admin.site.urls)),

    # Bookings urls
    url(r'^bookings/', include('bookings.urls')),

    # Robots.txt
    (r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain"))
)

urlpatterns += staticfiles_urlpatterns()
