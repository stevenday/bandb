from calendar import HTMLCalendar
from datetime import timedelta

"""
Helper generator function to return the days in a particular month
occupied by a queryset of models with start and end date fields
"""
def occupied_days(self, queryset, year, month):
    for model in queryset:
        for day in daterange(model.start, model.end):
            # Some of the models passed might overlap from a previous month
            if day.year == year and day.month == month:
                yield day

"""
Helper generator function to return the dates represented by a date range
"""
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

class BookingCalendar(HTMLCalendar):
    """
    Extend python's HTMLCalendar to colour in cells based on whether there's
    a booking on that day
    """

    def __init__(self, year, month):
        super(BookingCalendar, self).__init__()
        self.booked_days = occupied_days(Booking.objects.bookings_in_month(year, month), year, month)
        self.holiday_days = occupied_days(Holiday.objects.holidays_in_month(year, month), year, month)

    def formatday(self, day, weekday):
        """
        Format the table cell for a particular day
        """
        cssclass = "available"
        if day in self.booked_days:
            cssclass = "booked"
        elif day in self.holiday_days:
            cssclass = "unavailable"
        return self.day_cell(cssclass, day)

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)