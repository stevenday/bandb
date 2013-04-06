(function(window, $) {
    var dateFormat = 'DD/MM/YYYY';
    var $startInput = $("#id_start");
    var $endInput = $("#id_end");
    var $all_days = $('.calendar td.non-empty-day');

    var dayClick = function (event, $input) {
        event.preventDefault();
        var $cell = $(event.target);
        if (isAvailable($cell)) {
            // Highlight the date
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

    var isAvailable = function($cell, $input) {
        return $cell.hasClass("available");
    }

    $(".first-month td").click(function(e) {
        dayClick(e, $startInput);
    });

    $(".second-month td").click(function(e) {
        dayClick(e, $endInput);
    });

})(window, window.jQuery);