from datetime import datetime, timedelta, date

from django.test import TestCase
from django.core.exceptions import ValidationError

from ..models import Booking, Holiday
from .helpers import BookingTestCase

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

    def test_nights(self):
        start = datetime.now().date()
        end = start + timedelta(days=1)
        booking = Booking(start=start, end=end)
        self.assertEqual(booking.nights, 1)
        booking.end = booking.end + timedelta(days=1)
        self.assertEqual(booking.nights, 2)

    def test_price_methods(self):
        with self.settings(PRICE_PER_NIGHT=50):
            start = datetime.now().date()
            end = start + timedelta(days=1)
            booking = Booking(start=start, end=end)
            self.assertEqual(booking.price, 5000)
            self.assertEqual(booking.price_pounds, 50)
            booking.end = booking.end + timedelta(days=1)
            self.assertEqual(booking.price, 10000)
            self.assertEqual(booking.price_pounds, 100)


class BookingManagerTests(BookingTestCase):

    def setUp(self):
        self.create_bookings()

    def test_bookings_in_month(self):
        self.compare_querysets(Booking.objects.bookings_in_month(2013, 1), self.bookings_this_month)
        self.compare_querysets(Booking.objects.bookings_in_month(2012, 12), self.bookings_last_month)
        self.compare_querysets(Booking.objects.bookings_in_month(2013, 2), self.bookings_next_month)

    def test_bookings_in_month_excludes_unpaid_bookings(self):
        # Add a new booking which is unpaid
        start = date(2013, 1, 12)
        end = start + timedelta(days=1)
        Booking.objects.create(start=start, end=end, paid=False)
        self.compare_querysets(Booking.objects.bookings_in_month(2013, 1), self.bookings_this_month)

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

class HolidayManagerTests(BookingTestCase):

    def setUp(self):
        self.create_holidays()

    def test_holidays_in_month(self):
        self.compare_querysets(Holiday.objects.holidays_in_month(2013, 1), self.holidays_this_month)
        self.compare_querysets(Holiday.objects.holidays_in_month(2012, 12), self.holidays_last_month)
        self.compare_querysets(Holiday.objects.holidays_in_month(2013, 2), self.holidays_next_month)
