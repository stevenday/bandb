from datetime import datetime, date

from django.core.urlresolvers import reverse
from django.http import Http404
from django.views.generic import TemplateView
from django.views.generic.dates import YearMixin, MonthMixin
from django.utils.timezone import utc
from django.utils.safestring import mark_safe

from bookings.lib import BookingCalendar, next_year_month, previous_year_month

class HomeView(TemplateView):
    template_name = 'index.html'

class HutView(TemplateView):
    template_name = 'hut.html'

class RatesView(YearMixin, MonthMixin, TemplateView):
    template_name = 'rates.html'

    def get_year(self):
        year = super(RatesView, self).get_year()
        current_year = datetime.now().year
        if not year:
            year = current_year
        year = int(year)
        if year <= 0 or year < current_year:
            raise Http404
        return year

    def get_month(self):
        month = super(RatesView, self).get_month()
        if not month:
            month = datetime.now().month
        month = int(month)
        if month <= 0 or month > 12:
            raise Http404
        return month

    def get_context_data(self, **kwargs):
        context = super(RatesView, self).get_context_data(**kwargs)
        year = self.get_year()
        month = self.get_month()
        second_year, second_month = next_year_month(year, month)

        # We show two calendars, but hide one on small screens
        # so we have to make some redundant links that'll get
        # hidden if the second calendar is visible
        first_prev_year, first_prev_month = previous_year_month(year, month)
        first_prev_link = reverse('rates', kwargs={'year':first_prev_year, 'month':"%02d" % first_prev_month})
        first_next_link = reverse('rates', kwargs={'year':second_year, 'month':"%02d" % second_month})

        second_prev_link = reverse('rates', kwargs={'year':year, 'month':"%02d" % month})
        second_next_year, second_next_month = next_year_month(second_year, second_month)
        second_next_link = reverse('rates', kwargs={'year':second_next_year, 'month':"%02d" % second_next_month})

        calendar = BookingCalendar(year, month, prev_link=first_prev_link, next_link=first_next_link)
        second_calendar = BookingCalendar(second_year, second_month, prev_link=second_prev_link, next_link=second_next_link)

        context['first_bookings'] = mark_safe(calendar.formatmonth(year, month, withyear=True))
        context['second_bookings'] = mark_safe(second_calendar.formatmonth(second_year, second_month, withyear=True))

        return context

class AreaView(TemplateView):
    template_name = 'area.html'

class ThingsToKnowView(TemplateView):
    template_name = 'things-to-know.html'