from datetime import datetime, date

from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.dates import YearMixin, MonthMixin
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from django.utils.timezone import utc
from django.utils.safestring import mark_safe
from django.http import Http404, HttpResponse
from django.conf import settings

from .models import Booking
from .forms import BookingCreateForm, PaymentForm
from .lib import BookingCalendar, next_year_month, previous_year_month

class BookingCalendarMixin(YearMixin, MonthMixin):
    """
    Mixin for views which want to show a single booking calendar
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

    def get_selected(self):
        try:
            return datetime.strptime(self.request.GET.get('date'), '%d/%m/%Y').date()
        except (ValueError, TypeError):
            return None


    def get_context_data(self, **kwargs):
        context = super(BookingCalendarMixin, self).get_context_data(**kwargs)
        year = self.get_year()
        month = self.get_month()
        selected_date = self.get_selected()
        prev_year, prev_month = previous_year_month(year, month)
        next_year, next_month = next_year_month(year, month)

        prev_link = reverse(self.url_name, kwargs={'year':prev_year, 'month':"%02d" % prev_month})
        next_link = reverse(self.url_name, kwargs={'year':next_year, 'month':"%02d" % next_month})

        calendar = BookingCalendar(year, month, prev_link=prev_link, next_link=next_link, selected_date=selected_date)

        context['calendar'] = mark_safe(calendar.formatmonth(year, month, withyear=True))

        return context


class BookingsView(BookingCalendarMixin, TemplateView):
    template_name = 'bookings.html'
    url_name = 'bookings'


class BookingCalendarAjax(BookingCalendarMixin, TemplateView):
    url_name = 'bookings'

    def render_to_response(self, context, **response_kwargs):
        print "rendering calendar to response"
        # We only want to return the html for the calendar
        return HttpResponse(context['calendar'], **response_kwargs)


class CreateBooking(BookingCalendarMixin, CreateView):
    model = Booking
    template_name = 'booking_create.html'
    form_class = BookingCreateForm
    url_name = 'booking'

    def get_selected(self):
        """
        Override get_selected to return the initial data' selected value instead
        """
        # POST overrides GET because it's the user's submission from this page
        submitted_date = None
        if self.request.POST.get('start'):
            print "POST has a better date"
            submitted_date = self.request.POST.get('start')
        elif self.request.GET.get('date'):
            print "GET has a date"
            submitted_date = self.request.GET.get('date')

        try:
            return datetime.strptime(submitted_date, '%d/%m/%Y').date()
        except (ValueError, TypeError):
            return None

    def get_success_url(self):
        return reverse('payment', kwargs={'pk':self.object.id})

    def get_initial(self):
        initial = super(CreateBooking, self).get_initial()
        initial['start'] = self.get_selected()
        return initial


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
