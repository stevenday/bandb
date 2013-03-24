from datetime import datetime

from django.db import models
from django.core.exceptions import ValidationError

class Booking(models.Model):

    name = models.CharField(max_length=255, help_text='A name to help you remember this booking - eg: the guests\' name.')
    start = models.DateField(help_text='Which day does the booking start?')
    end = models.DateField(help_text='Which day does the booking end?')

    def clean(self):
        if self.start >= self.end:
            raise ValidationError('The booking start must be before the end.')
        elif self.start < datetime.now().date():
            raise ValidationError('The booking has to start today or later.')

    def __unicode__(self):
        return "{0}, from: {1} to: {2}".format(self.name, self.start, self.end)

class Holiday(models.Model):

    name = models.CharField(max_length=255, help_text='A name to help you remember this holiday.')
    start = models.DateField(help_text='Which day does the holiday start?')
    end = models.DateField(help_text='Which day does the holiday end?')

    def clean(self):
        if self.start >= self.end:
            raise ValidationError('The holiday start must be before the end.')
        elif self.start < datetime.now().date():
            raise ValidationError('The holiday has to start today or later.')

    def __unicode__(self):
        return "{0}, from: {1} to: {2}".format(self.name, self.start, self.end)

