(function(window, $, PhotoSwipe){

    $(document).ready(function(){

        var options = {
            getImageCaption: function(el) {
                return $(el).attr("data-caption");
            },
            captionAndToolbarAutoHideDelay: 0
        };

        var gallery = $(".gallery a").photoSwipe(options);

        $("a.gallery").click(function() {
            gallery.show(0);
        });

    });

}(window, window.jQuery, window.Code.PhotoSwipe));