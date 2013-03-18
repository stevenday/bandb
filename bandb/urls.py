from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponse

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from .views import *

urlpatterns = patterns('',
    # Examples:
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^hut$', HutView.as_view(), name='hut'),
    url(r'^rates$', RatesView.as_view(), name='rates'),
    url(r'^area$', AreaView.as_view(), name='area'),
    url(r'^availability$', AvailabilityView.as_view(), name='availability'),
    url(r'^things-to-know$', ThingsToKnowView.as_view(), name='things_to_know'),
    url(r'^find-us$', FindView.as_view(), name='find'),
    url(r'^gallery$', GalleryView.as_view(), name='gallery'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    # Robots.txt
    (r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain"))
)

urlpatterns += staticfiles_urlpatterns()
