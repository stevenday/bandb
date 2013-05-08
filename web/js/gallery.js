(function(window, $, PhotoSwipe){

    $(document).ready(function(){

        var options = {
            getImageCaption: function(el) {
                return $(el).attr("data-caption");
            },
            captionAndToolbarAutoHideDelay: 0,
            captionAndToolbarShowEmptyCaptions: false,
            jQueryMobile: false,
            loop: false,
            preventSlideshow: true
        };

        var gallery = $(".gallery a").photoSwipe(options);

        $("a.gallery").click(function(e) {
            e.preventDefault();
            gallery.show(0);
        });

    });

}(window, window.jQuery, window.Code.PhotoSwipe));