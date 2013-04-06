from django.views.generic import TemplateView

from bookings.views import BookingCalendarMixin

class HomeView(TemplateView):
    template_name = 'index.html'

class HutView(TemplateView):
    template_name = 'hut.html'

class RatesView(BookingCalendarMixin, TemplateView):
    template_name = 'rates.html'
    url_name = 'rates'

class AreaView(TemplateView):
    template_name = 'area.html'

class ThingsToKnowView(TemplateView):
    template_name = 'things-to-know.html'