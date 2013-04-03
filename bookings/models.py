from datetime import datetime

from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError

class BookingManager(models.Manager):

    def bookings_in_month(self, year, month):
        """
        Bookings which start or end in the given month
        """
        return super(BookingManager, self).all().filter(Q(start__year=year, start__month=month) | Q(end__year=year, end__month=month))

class Booking(models.Model):

    objects = BookingManager()

    name = models.CharField(max_length=255, help_text='A name to help you remember this booking - eg: the guests\' name.')
    start = models.DateField(db_index=True, help_text='Which day does the booking start?')
    end = models.DateField(db_index=True, help_text='Which day does the booking end?')
    email = models.EmailField(max_length=255, help_text='What is the guest\'s email address?')
    notes = models.TextField(blank=True, help_text='Any extra notes from the guest about their booking')
    paid = models.BooleanField(default=False, help_text='Has this booking been paid for?')

    def clean(self):
        if self.start >= self.end:
            raise ValidationError('The booking start must be before the end.')
        elif self.start < datetime.now().date():
            raise ValidationError('The booking has to start today or later.')

    def __unicode__(self):
        return "{1} to: {2}, {3:.2f}".format(self.name, self.start, self.end, self.price_pounds)

    @property
    def price(self):
        """
        Return the price in pence.
        """
        # TODO, calculate from days and price per day in settings?
        return 18500

    @property
    def price_pounds(self):
        return self.price / 100

class HolidayManager(models.Manager):

    def holidays_in_month(self, year, month):
        """
        Holidays which start or end in the given month
        """
        return super(HolidayManager, self).all().filter(Q(start__year=year, start__month=month) | Q(end__year=year, end__month=month))

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
