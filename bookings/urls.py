from django.conf.urls import patterns, include, url
from django.views.decorators.csrf import csrf_exempt

from .views import *

urlpatterns = patterns('',
    url(r'^$', CreateBooking.as_view(), name='booking'),
    url(r'^(?P<pk>\d+)/pay$', csrf_exempt(PayForBooking.as_view()), name='payment')
)
