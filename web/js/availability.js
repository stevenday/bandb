(function(window, $){
    $(function(){
        var bindCalendarLinks = function() {
            $(".non-empty-day").click(function(e){
                e.preventDefault
                clicked = e.target
                if($(clicked).hasClass("available")) {
                    alert("That day is available.")
                }

                if($(clicked).hasClass("booked")) {
                    alert("That day is already booked.");
                }

                if($(clicked).hasClass("unavailable")) {
                    alert("We're not open for bookings on that day.");
                }
            });
        }

        bindCalendarLinks();
        $(document).on('NewCalendar', bindCalendarLinks);
    });
})(window, window.jQuery);