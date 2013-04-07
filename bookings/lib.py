from calendar import HTMLCalendar, month_name, monthrange
from datetime import datetime, timedelta, date

from .models import Booking, Holiday

"""
Helper function to return the days in a particular month
occupied by a queryset of models with start and end date fields
"""
def occupied_days(queryset, year, month):
    days = []
    for model in queryset:
        for day in daterange(model.start, model.end):
            # Some of the models passed might overlap from a previous month
            if day.year == year and day.month == month and not date in days:
                days.append(day.day)
    return days

"""
Helper function to return the dates represented by a date range
"""
def daterange(start_date, end_date):
    dates = []
    for n in range(int ((end_date - start_date).days)):
        dates.append(start_date + timedelta(n))
    return dates

def previous_year_month(year, month):
    prev_month = (month - 1) if month > 1 else 12
    prev_year = year if month > 1 else (year - 1)
    return (prev_year, prev_month)

def next_year_month(year, month):
    next_month = (month + 1) if month < 12 else 1
    next_year = year if month < 12 else (year + 1)
    return (next_year, next_month)

class BookingCalendar(HTMLCalendar):
    """
    Extend python's HTMLCalendar to colour in cells based on whether there's
    a booking on that day
    """

    def __init__(self, year, month, prev_link=None, next_link=None):
        super(BookingCalendar, self).__init__()
        self.year = year
        self.month = month
        self.today = datetime.now().date()
        self.prev_link = prev_link
        if self.prev_link:
            self.prev_year, self.prev_month = previous_year_month(year, month)
        self.next_link = next_link
        if self.next_link:
            self.next_year, self.next_month = next_year_month(year, month)
        self.booked_days = occupied_days(Booking.objects.bookings_in_month(year, month), year, month)
        self.holiday_days = occupied_days(Holiday.objects.holidays_in_month(year, month), year, month)

    def formatmonthname(self, theyear, themonth, withyear=False):
        """
        Return a month name as a table row. With optional prev/next links
        """
        if withyear:
            s = '%s %s' % (month_name[themonth], theyear)
        else:
            s = '%s' % month_name[themonth]

        prev = ''
        next = ''

        if self.prev_link:
            prev = '<a href="{0}" class="calendar-link">&lt;&lt; {1}</a>'.format(self.prev_link, month_name[self.prev_month])

        if self.next_link:
            next = '<a href="{0}" class="calendar-link">{1} &gt;&gt;</a>'.format(self.next_link, month_name[self.next_month])

        return '<tr><th colspan="7" class="heading text--center"><span class="prev float--left">{0}</span><span class="month">{1}</span><span class="next float--right">{2}</span></th></tr>'.format(prev, s, next)


    def formatday(self, day, weekday):
        """
        Format the table cell for a particular day
        """

        cssclasses = ["day"]
        full_date = None
        if day <= 0:
            # We get empty days with day = 0 or day > days in month
            pass
        else:
            cssclasses.append("non-empty-day")

            full_date = date(self.year, self.month, day)

            if full_date < self.today or day in self.holiday_days:
                cssclasses.append("unavailable")
            elif day in self.booked_days:
                cssclasses.append("booked")
            else:
                cssclasses.append("available")

            if full_date == self.today:
                cssclasses.append("today")
        return self.day_cell(' '.join(cssclasses), day, full_date)

    def day_cell(self, cssclass, day, full_date=None):
        if full_date:
            date_string = full_date.isoformat()
            return '<td data-date="{0}" class="{1}">{2}</td>'.format(date_string, cssclass, day)
        else:
            return '<td class="{0}"></td>'.format(cssclass)