from datetime import date, datetime, timedelta
from calendar import monthrange

from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.conf import settings

class BookingManager(models.Manager):

    def confirmed_bookings(self):
        """
        Bookings which have been paid for
        """
        return super(BookingManager, self).all().filter(paid=True)

    def bookings_in_month(self, year, month):
        """
        Bookings which start, end or span the given month
        """
        # Calculate the days at the start/end of the month
        month_range = monthrange(year, month)
        start_of_month = 1
        end_of_month = month_range[1]
        # Filter out bookings which end before this month or start after it
        return self.confirmed_bookings().filter(
            ~Q(end__lt=date(year, month, start_of_month)) |
            ~Q(start__gt=date(year, month, end_of_month))
        )

    def dates_available(self, start, end):
        """
        Are the dates between start and end available?
        They are available if there are no confirmed bookings overlapping any
        of the days
        """
        # We have to do a bit of fudging to make this a simple/efficient db query
        # because one booking can start on the day another ends, which __range
        # doesn't quite get.
        day_before_end = end - timedelta(days=1)
        day_after_start = start + timedelta(days=1)
        return not self.confirmed_bookings().filter(
            Q(start__range=(start, day_before_end)) |
            Q(end__range=(day_after_start, end))
        ).exists()

    def bookings_to_email(self):
        """
        Return bookings which need emailing
        """
        return self.confirmed_bookings().filter(
            Q(guest_emails_sent=False) |
            Q(host_emails_sent=False)
        )

class Booking(models.Model):

    objects = BookingManager()

    name = models.CharField(max_length=255, help_text='A name to help you remember this booking - eg: the guests\' name.')
    start = models.DateField(db_index=True, help_text='Which day does the booking start?')
    end = models.DateField(db_index=True, help_text='Which day does the booking end?')
    email = models.EmailField(max_length=255, help_text='What is the guest\'s email address?')
    notes = models.TextField(blank=True, help_text='Any extra notes from the guest about their booking')
    paid = models.BooleanField(default=False, help_text='Has this booking been paid for?')
    # A flag to say that emails have been sent to the host
    guest_emails_sent = models.BooleanField(default=False, help_text='Have the emails been sent to the guest confirm this booking? If you don\'t tick it, an email will be sent to the guest!')
    host_emails_sent = models.BooleanField(default=False, help_text='Have the emails been sent to the host to confirm this booking? If you don\'t tick it, an email will be sent to the host!')

    def clean(self):
        # Check basics about start/end dates being valid
        if self.start >= self.end:
            raise ValidationError('The booking start must be before the end.')
        elif self.start < datetime.now().date():
            raise ValidationError('The booking has to start today or later.')

        # Check availability
        # Don't let people make a booking on the same day as a confirmed booking
        if not Booking.objects.dates_available(start=self.start, end=self.end):
            raise ValidationError('Some or all of those dates are not available')


    def __unicode__(self):
        return "{0} - {1} to: {2}, {3:.2f}".format(self.name, self.start, self.end, self.price_pounds)

    @property
    def nights(self):
        """
        Return how many nights the booking is for
        """
        return (self.end - self.start).days

    @property
    def price(self):
        """
        Return the price in pence.
        """
        # PRICE_PER_NIGHT is specified in whole pounds
        return self.nights * settings.PRICE_PER_NIGHT * 100

    @property
    def price_pounds(self):
        return self.price / 100

    @property
    def remaining(self):
        return self.price_pounds - settings.DEPOSIT

class HolidayManager(models.Manager):

    def holidays_in_month(self, year, month):
        """
        Holidays which start, end or span the given month
        """
        # Calculate the days at the start/end of the month
        month_range = monthrange(year, month)
        start_of_month = 1
        end_of_month = month_range[1]
        # Filter out holidays which end before this month or start after it
        return super(HolidayManager, self).all().filter(
            ~Q(end__lt=date(year, month, start_of_month)) |
            ~Q(start__gt=date(year, month, end_of_month))
        )

class Holiday(models.Model):

    objects = HolidayManager()

    name = models.CharField(max_length=255, help_text='A name to help you remember this holiday.')
    start = models.DateField(db_index=True, help_text='Which day does the holiday start?')
    end = models.DateField(db_index=True, help_text='Which day does the holiday end?')

    def clean(self):
        if self.start >= self.end:
            raise ValidationError('The holiday start must be before the end.')
        elif self.start < datetime.now().date():
            raise ValidationError('The holiday has to start today or later.')

    def __unicode__(self):
        return "{0}, from: {1} to: {2}".format(self.name, self.start, self.end)
