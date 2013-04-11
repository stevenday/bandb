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

    def test_checks_availability(self):
        # Only a simple check to make sure we call something, the real
        # checks of the function we call are in BookingManagerTests.test_dates_available
        start = datetime.now().date()
        end = start + timedelta(days=3)
        booking = Booking.objects.create(start=start, end=end, paid=True)
        second_booking = Booking.objects.create(start=start, end=end, paid=True)
        with self.assertRaises(ValidationError) as context:
            second_booking.clean();

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

    def test_bookings_in_month(self):
        self.create_bookings()
        self.compare_querysets(Booking.objects.bookings_in_month(2013, 1), self.bookings_this_month)
        self.compare_querysets(Booking.objects.bookings_in_month(2012, 12), self.bookings_last_month)
        self.compare_querysets(Booking.objects.bookings_in_month(2013, 2), self.bookings_next_month)

    def test_bookings_in_month_excludes_unpaid_bookings(self):
        self.create_bookings()
        # Add a new booking which is unpaid
        start = date(2013, 1, 12)
        end = start + timedelta(days=1)
        Booking.objects.create(start=start, end=end, paid=False)
        self.compare_querysets(Booking.objects.bookings_in_month(2013, 1), self.bookings_this_month)

    def test_dates_available(self):
        self.create_bookings()
        # Test all the possible combinations of start/end date
        number_of_nights = (1, 2, 3, 4, 5, 6)
        bigger_number_of_nights = (1, 2, 3, 4, 5, 6, 7)
        for nights in number_of_nights:
            # Create a booking with that many nights
            start = datetime.now().date()
            end = start + timedelta(days=nights)
            booking = Booking.objects.create(start=start, end=end, paid=True)
            # Loop through all the possible ranges of nights within, intersecting or containg that
            # booking
            for start_offset in (-1, 0, 1, 2, 3, 4, 4, 5, 6, 7):
                test_start = start + timedelta(days=start_offset)
                for end_offset in bigger_number_of_nights:
                    test_end = start + timedelta(days=end_offset)

                if (test_start < start and test_end <= end) or (test_start >= end and test_end > end):
                    self.assertTrue(Booking.objects.dates_available(test_start, test_end),
                                    'Date range: {0} -> {1} should be available with booking: {2} but it\'s not'.format(test_start, test_end, booking))
                else:
                    self.assertFalse(Booking.objects.dates_available(test_start, test_end),
                                    'Date range: {0} -> {1} should not be available with booking: {2} but it is'.format(test_start, test_end, booking))
            # Tidy up the booking
            booking.delete()

    def test_bookings_to_email(self):
        start = datetime.now().date()
        end = start + timedelta(days=1)
        email = 'test@example.com'
        name = 'Guest'
        # An unconfirmed booking which should not be emailed
        unconfirmed_booking = Booking.objects.create(name=name, start=start, end=end, email=email, paid=False)
        # Add a booking which has not been emailed but should be
        booking_that_needs_emailing = Booking.objects.create(name=name, start=start, end=end, email=email, paid=True)
        # And a booking which has
        booking_thats_been_emailed = Booking.objects.create(name=name, start=start, end=end, email=email, paid=True, emails_sent=True)
        self.assertEqual(list(Booking.objects.bookings_to_email()), [booking_that_needs_emailing])


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
