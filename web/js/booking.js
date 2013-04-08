(function(window, $) {

    $(function() {
        var dateFormat = 'DD/MM/YYYY';
        var $startInput = $("#id_start");

        var isAvailable = function($cell, $input) {
            return $cell.hasClass("available");
        };

        var dayClick = function (event, $input) {
            event.preventDefault();
            var $cell = $(event.target);
            if (isAvailable($cell)) {
                // Highlight the date
                $("td.selected").toggleClass("selected");
                $cell.addClass("selected");
                // Parse the date from the calendar
                var date = moment($cell.attr('data-date'));
                // Update the input
                $input.val(date.format(dateFormat));
            }
            else {
                alert("Sorry, that day's already booked.");
            }
        }

        var bindCalendarLinks = function() {
            $(".calendar td").click(function(e) {
                dayClick(e, $startInput);
            });
        };

        bindCalendarLinks();
        $(document).on("NewCalendar", bindCalendarLinks);
    });

})(window, window.jQuery);