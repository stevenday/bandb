from datetime import timedelta, date, datetime

from django.test import TransactionTestCase

from ..models import Booking, Holiday

def create_test_booking(attributes={}):
    tomorrow = datetime.now().date() + timedelta(days=1)
    # Make a Booking with the bare minimum
    default_attributes = {
        'name': 'Test Booking',
        'start': tomorrow,
        'end': tomorrow + timedelta(days=2),
        'email': 'guest@example.com'
    }
    default_attributes.update(attributes)
    instance = Booking(**dict((k,v) for (k,v) in default_attributes.items() if '__' not in k))
    instance.save()
    return instance


class BookingTestCase(TransactionTestCase):

    def create_bookings(self):
        # Create some dates to use
        start_of_this_month = date(2013, 1, 1)
        end_of_this_month = date(2013, 1, 30)
        overlapping_this_month_next_month = date(2013, 1, 31)
        overlapping_last_month_this_month = date(2012, 12, 31)

        start_of_last_month = date(2012, 12, 1)
        end_of_last_month = date(2012, 12, 30)

        start_of_next_month = date(2013, 2, 1)
        end_of_next_month = date(2013, 2, 27)

        # Some arrays of dates to use
        this_month = [start_of_this_month,
                      end_of_this_month,
                      overlapping_this_month_next_month,
                      overlapping_last_month_this_month]
        next_month = [start_of_next_month, end_of_next_month]
        last_month = [start_of_last_month, end_of_last_month]

        # Use the above to create bookings for the days
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

        # Create some other more complicated bookings
        booking_spanning_exactly_whole_month = Booking.objects.create(start=start_of_this_month, end=end_of_this_month, paid=True)

        booking_spanning_over_middle_of_two_months = Booking.objects.create(start=date(2012, 1, 15), end=date(2012, 2, 15), paid=True)
        booking_spanning_over_two_months_from_exact_start = Booking.objects.create(start=start_of_this_month, end=date(2012, 2, 15), paid=True)
        booking_spanning_over_two_months_to_exact_end = Booking.objects.create(start=date(2012, 1, 10), end=end_of_next_month, paid=True)
        booking_spanning_exactly_two_months = Booking.objects.create(start=start_of_this_month, end=end_of_next_month, paid=True)

        self.bookings_this_month.append(booking_spanning_exactly_whole_month)
        self.bookings_this_month.append(booking_spanning_over_middle_of_two_months)
        self.bookings_this_month.append(booking_spanning_over_two_months_from_exact_start)
        self.bookings_this_month.append(booking_spanning_over_two_months_to_exact_end)
        self.bookings_this_month.append(booking_spanning_exactly_two_months)

        self.bookings_next_month.append(booking_spanning_over_middle_of_two_months)
        self.bookings_next_month.append(booking_spanning_over_two_months_from_exact_start)
        self.bookings_next_month.append(booking_spanning_over_two_months_to_exact_end)
        self.bookings_next_month.append(booking_spanning_exactly_two_months)

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

        # Create some other more complicated bookings
        # Should only be in this month
        holiday_spanning_exactly_whole_month = Holiday.objects.create(start=start_of_this_month, end=end_of_this_month)
        # Should be in this month and next month
        holiday_spanning_over_middle_of_two_months = Holiday.objects.create(start=date(2012, 1, 15), end=date(2012, 2, 15))
        # Should be in this month and next month
        holiday_spanning_over_two_months_from_exact_start = Holiday.objects.create(start=start_of_this_month, end=date(2012, 2, 15))
        # Should be in this month and next month
        holiday_spanning_over_two_months_to_exact_end = Holiday.objects.create(start=date(2012, 1, 10), end=end_of_next_month)
        # Should be in this month and next month
        holiday_spanning_exactly_two_months = Holiday.objects.create(start=start_of_this_month, end=end_of_next_month)

        self.holidays_this_month.append(holiday_spanning_exactly_whole_month)
        self.holidays_this_month.append(holiday_spanning_over_middle_of_two_months)
        self.holidays_this_month.append(holiday_spanning_over_two_months_from_exact_start)
        self.holidays_this_month.append(holiday_spanning_over_two_months_to_exact_end)
        self.holidays_this_month.append(holiday_spanning_exactly_two_months)

        self.holidays_next_month.append(holiday_spanning_over_middle_of_two_months)
        self.holidays_next_month.append(holiday_spanning_over_two_months_from_exact_start)
        self.holidays_next_month.append(holiday_spanning_over_two_months_to_exact_end)
        self.holidays_next_month.append(holiday_spanning_exactly_two_months)

    def compare_querysets(self, actual, expected):
        #self.assertEqual(len(actual), len(expected))
        for model in expected:
            self.assertTrue(model in actual, "{0} is not in {1}".format(model, actual))
