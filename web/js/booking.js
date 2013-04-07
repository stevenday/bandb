(function(window, $) {
    var dateFormat = 'DD/MM/YYYY';
    var $startInput = $("#id_start");
    var $endInput = $("#id_end");

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

    var isAvailable = function($cell, $input) {
        return $cell.hasClass("available");
    }

    $(".calendar td").click(function(e) {
        dayClick(e, $startInput);
    });

})(window, window.jQuery);