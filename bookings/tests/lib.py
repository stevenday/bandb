from django.test import TestCase

from ..lib import occupied_days
from ..models import Booking, Holiday
from .helpers import BookingTestCase

def LibTests(TestCase):
    def test_occupied_days(self):
        self.create_bookings()

        expected_this_month = [1, 2, 30, 31]
        expected_last_month = [1, 2, 30, 31]
        expected_next_month = [1, 2, 27]

        occupied_days_this_month = occupied_days(self.bookings_this_month)
        for day in occupied_days_this_month:
            self.assertTrue(day in expected_this_month)

        occupied_days_this_month = occupied_days(self.bookings_last_month)
        for day in occupied_days_last_month:
            self.assertTrue(day in expected_last_month)

        occupied_days_next_month = occupied_days(self.bookings_next_month)
        for day in occupied_days_next_month:
            self.assertTrue(day in expected_next_month)