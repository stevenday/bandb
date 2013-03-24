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

    def clean(self):
        if self.start >= self.end:
            raise ValidationError('The booking start must be before the end.')
        elif self.start < datetime.now().date():
            raise ValidationError('The booking has to start today or later.')

    def __unicode__(self):
        return "{0}, from: {1} to: {2}".format(self.name, self.start, self.end)

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
