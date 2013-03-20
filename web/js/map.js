(function(L){
    var latLon = [50.985397, -2.174799]
    var map = L.map('map').setView(latLon, 13);
    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    L.marker(latLon).addTo(map)
        .bindPopup('Tilley\'s Hut')
        .openPopup();
 })(window.L);