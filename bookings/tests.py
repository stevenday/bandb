from datetime import datetime, timedelta

from django.test import TestCase
from django.core.exceptions import ValidationError

from .models import Booking

class BookingTests(TestCase):

    def test_start_must_be_before_end(self):
        start = datetime.now().date()
        end = start - timedelta(days=1)
        booking = Booking(start=start, end=end)
        with self.assertRaises(ValidationError) as context:
            booking.clean()

    def test_start_must_not_be_in_the_past(self):
        start = datetime.now().date() - timedelta(days=1)
        end = start + timedelta(days=1)
        booking = Booking(start=start, end=end)
        with self.assertRaises(ValidationError) as context:
            booking.clean()

class HolidayTests(TestCase):

    def test_start_must_be_before_end(self):
        start = datetime.now().date()
        end = start - timedelta(days=1)
        holiday = Holiday(start=start, end=end)
        with self.assertRaises(ValidationError) as context:
            holiday.clean()

    def test_start_must_not_be_in_the_past(self):
        start = datetime.now().date() - timedelta(days=1)
        end = start + timedelta(days=1)
        holiday = Holiday(start=start, end=end)
        with self.assertRaises(ValidationError) as context:
            holiday.clean()
