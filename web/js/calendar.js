(function(window, $){

    var bindCalendarLinks = function() {
        $(".calendar-link").click(function(e) {
            e.preventDefault();
            // Split out the month and year
            var url = $(e.target).attr('href');
            var urlParts = url.split("/");
            var year = urlParts[urlParts.length-2];
            var month = urlParts[urlParts.length-1];
            $.ajax({
                url: '/bookings/ajax/' + year + '/' + month,
                dataType: 'html',
                success: function(data, textStatus, jqXHR) {
                    $(".calendar").html(data);
                    $(document).trigger("NewCalendar");
                }
            });
        });
    };

    $(function(){
        bindCalendarLinks();
        $(document).on("NewCalendar", bindCalendarLinks);
    });
})(window, window.jQuery);