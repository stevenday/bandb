$(function(){

    enableDatePickers();

    function enableDatePickers(){
        // Datepickers
        var sharedOptions = {
            format:'dd/mm/yyyy',
            weekStart: 1,
            autoclose: true
        };

        var nextFriday = new Date().next().friday().toString('dd/MM/yyyy');
        var nextSunday = new Date().next().friday().add({days:3}).toString('dd/MM/yyyy');

        $("input.date").datepicker(sharedOptions);
        $("#start-date").val(nextFriday).datepicker('setStartDate', nextFriday);
        $("#end-date").val(nextSunday).datepicker('setStartDate', nextSunday);

        $("#start-date").on("changeDate", function(e) {
            dateString = $("#start_date").val();
            $("#end-date").val(dateString).datepicker("setStartDate", dateString);
        });

        $("#inline-calendar-1").datepicker(sharedOptions).datepicker('show');
        $("#inline-calendar-2").datepicker(sharedOptions).datepicker('show');
    }
});