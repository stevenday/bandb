from datetime import datetime, date

from django.views.generic.edit import CreateView, FormView
from django.views.generic.dates import YearMixin, MonthMixin
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from django.utils.timezone import utc
from django.utils.safestring import mark_safe
from django.http import Http404

from .models import Booking
from .forms import BookingCreateForm, PaymentForm
from .lib import BookingCalendar, next_year_month, previous_year_month

class BookingCalendarMixin(YearMixin, MonthMixin):
    """
    Mixin for views which want to show booking calendars
    """
    def get_year(self):
        year = super(BookingCalendarMixin, self).get_year()
        current_year = datetime.now().year
        if not year:
            year = current_year
        year = int(year)
        if year <= 0 or year < current_year:
            raise Http404
        return year

    def get_month(self):
        month = super(BookingCalendarMixin, self).get_month()
        if not month:
            month = datetime.now().month
        month = int(month)
        if month <= 0 or month > 12:
            raise Http404
        return month

    def get_context_data(self, **kwargs):
        context = super(BookingCalendarMixin, self).get_context_data(**kwargs)
        year = self.get_year()
        month = self.get_month()
        second_year, second_month = next_year_month(year, month)

        # We show two calendars, but we can hide one on small screens
        # so we have to make some redundant links that'll get
        # hidden if the second calendar is visible
        first_prev_year, first_prev_month = previous_year_month(year, month)
        first_prev_link = reverse(self.url_name, kwargs={'year':first_prev_year, 'month':"%02d" % first_prev_month})
        first_next_link = reverse(self.url_name, kwargs={'year':second_year, 'month':"%02d" % second_month})

        second_prev_link = reverse(self.url_name, kwargs={'year':year, 'month':"%02d" % month})
        second_next_year, second_next_month = next_year_month(second_year, second_month)
        second_next_link = reverse(self.url_name, kwargs={'year':second_next_year, 'month':"%02d" % second_next_month})

        calendar = BookingCalendar(year, month, prev_link=first_prev_link, next_link=first_next_link)
        second_calendar = BookingCalendar(second_year, second_month, prev_link=second_prev_link, next_link=second_next_link)

        context['first_bookings'] = mark_safe(calendar.formatmonth(year, month, withyear=True))
        context['second_bookings'] = mark_safe(second_calendar.formatmonth(second_year, second_month, withyear=True))

        return context

class CreateBooking(BookingCalendarMixin, CreateView):
    model = Booking
    template_name = 'booking_create.html'
    form_class = BookingCreateForm
    url_name = 'booking'

    def get_success_url(self):
        return reverse('payment', kwargs={'pk':self.object.id})

class PayForBooking(FormView):
    form_class = PaymentForm
    template_name = 'booking_payment.html'
    confirm_template = 'booking_payment_confirm.html'

    def get_initial(self):
        initial = super(PayForBooking, self).get_initial()
        # Try to get an unpaid booking with the supplied id
        booking = get_object_or_404(Booking, pk=self.kwargs['pk'], paid=False)
        initial['booking_id'] = booking.id
        return initial

    def get_context_data(self, **kwargs):
        context = super(PayForBooking, self).get_context_data(**kwargs)
        context['booking'] = Booking.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        # If we get here, we have been paid!
        booking = Booking.objects.get(pk=form.cleaned_data['booking_id'])
        booking.paid = True
        booking.save()

        # Show a confirmation page
        context = RequestContext(self.request)
        context['booking'] = booking
        return render(self.request, self.confirm_template, context)