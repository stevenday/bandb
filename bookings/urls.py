from django.conf.urls import patterns, include, url
from django.views.decorators.csrf import csrf_exempt

from .views import *

urlpatterns = patterns('',
    url(r'^(?:/(?P<year>\d{4})/(?P<month>\d{2}))?$', BookingsView.as_view(), name='bookings'),
    url(r'^ajax(?:/(?P<year>\d{4})/(?P<month>\d{2}))?$', BookingCalendarAjax.as_view(), name='bookings-ajax'),
    url(r'^new(?:/(?P<year>\d{4})/(?P<month>\d{2}))?$', CreateBooking.as_view(), name='booking'),
    url(r'^(?P<pk>\d+)/pay$', csrf_exempt(PayForBooking.as_view()), name='payment')
)
