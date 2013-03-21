from calendar import HTMLCalendar

class BookingCalendar(HTMLCalendar):
    """
    Extend python's HTMLCalendar to colour in cells based on whether there's
    a booking on that day
    """

    def __init__(self, bookings, unavailable):
        super(BookingCalendar, self).__init__()
        self.bookings = bookings
        self.unavailable = unavailable

    def formatday(self, day, weekday):
        """
        Format the table cell for a particular day
        """
        cssclass = "available"
        if day in self.bookings:
            cssclass = "booked"
        elif day in self.unavailable:
            cssclass = "unavailable"
        return self.day_cell(cssclass, day)

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)


