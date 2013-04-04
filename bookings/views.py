from django.views.generic.edit import CreateView, FormView
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext

from .models import Booking
from .forms import BookingCreateForm, PaymentForm

class CreateBooking(CreateView):
    model = Booking
    template_name = 'booking_create.html'
    form_class = BookingCreateForm

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