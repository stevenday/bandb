from datetime import date
import calendar

from django.test.utils import override_settings

from .helpers import BookingTestCase
from ..models import Holiday
from ..lib import (
    occupied_days,
    default_holidays,
    apply_excluded_holidays,
    holiday_days
)

@override_settings(
    HOLIDAY_EXCEPTIONS=(
        date(2013, 1, 15),
        date(2013, 1, 16)
    ),
    DEFAULT_HOLIDAY_NIGHTS=(
        calendar.MONDAY,
        calendar.TUESDAY,
        calendar.WEDNESDAY,
        calendar.THURSDAY
    )
)
class LibTests(BookingTestCase):

    def setUp(self):
        # List of Mon-Thurs days in January 2013 used in several tests
        self.MIDWEEK_DAYS_IN_JAN_2013 = (1,2,3,7,8,9,10,14,15,16,17,21,22,23,24,28,29,30,31)

    def test_occupied_days(self):
        self.create_bookings()

        # Generate some sets of dates for testing the method with
        # Every day in January is booked
        expected_this_month = self.generate_date_set(2013, 1, range(1, 32))
        expected_last_month = self.generate_date_set(2012, 12, [1, 30, 31])
        # Every day in Feburary is booked
        expected_next_month = self.generate_date_set(2013, 2, range(1, 28))

        self.assertEqual(
            expected_this_month,
            occupied_days(self.bookings_this_month, 2013, 1)
        )
        self.assertEqual(
            expected_last_month,
            occupied_days(self.bookings_last_month, 2012, 12)
        )
        self.assertEqual(
            expected_next_month,
            occupied_days(self.bookings_next_month, 2013, 2)
        )
        # Check nothing is booked after this
        self.assertEqual(
            set(),
            occupied_days(self.bookings_next_month, 2013, 3)
        )


    def test_default_holidays(self):
        expected_default_holidays = self.generate_date_set(2013, 1, self.MIDWEEK_DAYS_IN_JAN_2013)
        actual_default_holidays = default_holidays(2013, 1)
        self.assertEqual(expected_default_holidays, actual_default_holidays)

    def test_apply_excluded_holidays(self):
        default_holidays = self.generate_date_set(2013, 1, self.MIDWEEK_DAYS_IN_JAN_2013)
        # Expected holidays after exclusions
        expected_holidays = default_holidays.copy()
        expected_holidays.remove(date(2013, 1, 15))
        expected_holidays.remove(date(2013, 1, 16))

        actual_holidays = apply_excluded_holidays(default_holidays)
        self.assertEqual(expected_holidays, actual_holidays)

    def test_holiday_days(self):
        default_holidays = self.generate_date_set(2013, 1, self.MIDWEEK_DAYS_IN_JAN_2013)
        expected_holidays = apply_excluded_holidays(default_holidays)
        # Create a manual holiday for the 15th which should override
        # the exclusions we've set up
        Holiday.objects.create(
            start=date(2013, 1, 15),
            end=date(2013, 1, 16)
        )
        # Manually add the 15th back into our expectations
        expected_holidays.add(date(2013, 1, 15))

        actual_holidays = holiday_days(2013, 1)

        self.assertEqual(expected_holidays, actual_holidays)

    def generate_date_set(self, year, month, days):
        """Generate a set of dates in the year and month given for the days
        given"""
        dates = set()
        for day in days:
            dates.add(date(year, month, day))
        return dates
