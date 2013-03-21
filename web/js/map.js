(function(window, L){
    var latLon = [50.985397, -2.174799]

    var map = L.map('map').setView(latLon, 14);

    L.tileLayer('http://{s}.tile.cloudmade.com/' + window.TilleysHut.CLOUDMADE_API_KEY + '/997/256/{z}/{x}/{y}.png', {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>',
        maxZoom: 18
    }).addTo(map);

    L.marker(latLon).addTo(map)
        .bindPopup('Tilley\'s Hut')
        .openPopup();
 })(window, window.L);