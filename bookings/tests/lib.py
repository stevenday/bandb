from .helpers import BookingTestCase
from ..lib import occupied_days

class LibTests(BookingTestCase):
    def test_occupied_days(self):
        self.create_bookings()

        expected_this_month = range(1, 32)  # Every day in January is booked
        expected_last_month = [1, 30, 31]
        expected_next_month = range(1, 28)  # Every day in Feburary is booked

        self.compare_occupied_days(
            expected_this_month,
            occupied_days(self.bookings_this_month, 2013, 1)
        )
        self.compare_occupied_days(
            expected_last_month,
            occupied_days(self.bookings_last_month, 2012, 12)
        )
        self.compare_occupied_days(
            expected_next_month,
            occupied_days(self.bookings_next_month, 2013, 2)
        )
        # Check nothing is booked after this
        self.compare_occupied_days(
            [],
            occupied_days(self.bookings_next_month, 2013, 3)
        )

    def compare_occupied_days(self, expected, actual):
        self.assertEqual(len(expected), len(actual), "Length of {0} does not match {1}".format(expected, actual))
        for day in actual:
            self.assertTrue(day in expected, "Expected day {0} is not in {1}".format(day, expected))
