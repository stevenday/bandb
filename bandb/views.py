import datetime

# Django imports
from django.views.generic import TemplateView
from django.utils.timezone import utc

from .lib import BookingCalendar

class HomeView(TemplateView):
    template_name = 'index.html'

class HutView(TemplateView):
    template_name = 'hut.html'

class RatesView(TemplateView):
    template_name = 'rates.html'

    def get_context_data(self, **kwargs):
        context = super(RatesView, self).setUp()
        # TODO - get some bookings from somewhere
        context['bookings'] = BookingCalendar([])
        return context

class AreaView(TemplateView):
    template_name = 'area.html'

class ThingsToKnowView(TemplateView):
    template_name = 'things-to-know.html'