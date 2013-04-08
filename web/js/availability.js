(function(window, $){
    $(function(){
        var bindCalendarLinks = function() {
            $(".non-empty-day").click(function(e){
                e.preventDefault
                $clicked = $(e.target)
                if($clicked.hasClass("available")) {
                    var make_booking = window.confirm("That day is available, would you like to make a booking?")
                    if (make_booking) {
                        var date = moment($clicked.attr('data-date'));
                        window.location = "/bookings/new/"
                                          + date.format("YYYY")
                                          + "/"
                                          + date.format("MM")
                                          + "?date="
                                          + encodeURIComponent(date.format("DD/MM/YYYY"));
                    }
                }

                if($(clicked).hasClass("booked")) {
                    window.alert("That day is already booked.");
                }

                if($(clicked).hasClass("unavailable")) {
                    window.alert("We're not open for bookings on that day.");
                }
            });
        }

        bindCalendarLinks();
        $(document).on('NewCalendar', bindCalendarLinks);
    });
})(window, window.jQuery);