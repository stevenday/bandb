from datetime import timedelta, date

from django.test import TransactionTestCase

from ..models import Booking, Holiday

class BookingTestCase(TransactionTestCase):

    def create_bookings(self):
        start_of_this_month = date(2013, 1, 1)
        end_of_this_month = date(2013, 1, 30)
        overlapping_this_month_next_month = date(2013, 1, 31)
        overlapping_last_month_this_month = date(2012, 12, 31)

        start_of_last_month = date(2012, 12, 1)
        end_of_last_month = date(2012, 12, 30)

        start_of_next_month = date(2013, 2, 1)
        end_of_next_month = date(2013, 2, 27)

        this_month = [start_of_this_month,
                      end_of_this_month,
                      overlapping_this_month_next_month,
                      overlapping_last_month_this_month]
        next_month = [start_of_next_month, end_of_next_month]
        last_month = [start_of_last_month, end_of_last_month]

        self.bookings_this_month = []
        for day in this_month:
            self.bookings_this_month.append(Booking.objects.create(start=day, end=day+timedelta(days=1), paid=True))

        self.bookings_last_month = []
        for day in last_month:
            self.bookings_last_month.append(Booking.objects.create(start=day, end=day+timedelta(days=1), paid=True))
        self.bookings_last_month += self.bookings_this_month[3:]

        self.bookings_next_month = []
        for day in next_month:
            self.bookings_next_month.append(Booking.objects.create(start=day, end=day+timedelta(days=1), paid=True))
        self.bookings_next_month += self.bookings_this_month[2:3]

    def create_holidays(self):
        start_of_this_month = date(2013, 1, 1)
        end_of_this_month = date(2013, 1, 30)
        overlapping_this_month_next_month = date(2013, 1, 31)
        overlapping_last_month_this_month = date(2012, 12, 31)

        start_of_last_month = date(2012, 12, 1)
        end_of_last_month = date(2012, 12, 30)

        start_of_next_month = date(2013, 2, 1)
        end_of_next_month = date(2013, 2, 27)

        this_month = [start_of_this_month,
                      end_of_this_month,
                      overlapping_this_month_next_month,
                      overlapping_last_month_this_month]
        next_month = [start_of_next_month, end_of_next_month]
        last_month = [start_of_last_month, end_of_last_month]

        self.holidays_this_month = []
        for day in this_month:
            self.holidays_this_month.append(Holiday.objects.create(start=day, end=day+timedelta(days=1)))

        self.holidays_last_month = []
        for day in last_month:
            self.holidays_last_month.append(Holiday.objects.create(start=day, end=day+timedelta(days=1)))
        self.holidays_last_month += self.holidays_this_month[3:]

        self.holidays_next_month = []
        for day in next_month:
            self.holidays_next_month.append(Holiday.objects.create(start=day, end=day+timedelta(days=1)))
        self.holidays_next_month += self.holidays_this_month[2:3]

    def compare_querysets(self, actual, expected):
        self.assertEqual(len(actual), len(expected))
        for model in expected:
            self.assertTrue(model in actual)