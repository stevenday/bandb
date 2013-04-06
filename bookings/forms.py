import stripe

from django import forms
from django.forms.widgets import HiddenInput, TextInput, DateInput
from django.conf import settings

from .models import Booking

class BookingCreateForm(forms.ModelForm):

    email = forms.CharField(widget=TextInput(attrs={'placeholder':'your-email@example.com'}))
    start = forms.DateField(widget=DateInput(attrs={'placeholder':'dd/mm/yyyy'}))
    end = forms.DateField(widget=DateInput(attrs={'placeholder':'dd/mm/yyyy'}))

    class Meta:
        model = Booking
        fields = [
            'name',
            'start',
            'end',
            'email',
            'notes'
        ]

class PaymentForm(forms.Form):

    booking_id = forms.IntegerField(required=True, widget=HiddenInput())
    stripe_token = forms.CharField(required=True, widget=HiddenInput())

    def clean(self):
        """
        Validate everything by trying to charge the card with Stripe
        """
        stripe.api_key = settings.STRIPE_SECRET_KEY
        # Get the credit card details submitted by the form
        token = self.cleaned_data['stripe_token']
        # Get the booking this relates to
        booking = Booking.objects.get(pk=self.cleaned_data['booking_id'])
        # Create the charge on Stripe's servers - this will charge the user's card
        try:
            charge = stripe.Charge.create(
                amount=booking.price, # Amount in pence
                currency="gbp",
                card=token,
                description=str(booking)
            )
            return self.cleaned_data
        except stripe.CardError, e:
            # The card has been declined
            raise forms.ValidationError("Sorry, your card has been declined. Perhaps you can try another?")
