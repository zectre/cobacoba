var map = L.map('map').setView([0, 0], 2);

var osmLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
});

var googleSatelliteLayer = L.tileLayer('https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}&key=YOUR_GOOGLE_MAPS_API_KEY', {
    maxZoom: 19,
});

osmLayer.addTo(map);

var baseLayers = {
    "OSM": osmLayer,
    "Google Satellite": googleSatelliteLayer,
};

L.control.layers(baseLayers).addTo(map);

var truckIcon = L.icon({
    iconUrl: 'https://www.pngmart.com/files/16/Vector-Dump-Truck-PNG-Free-Download.png',
    iconSize: [50, 50],
});

var locationLayer = L.realtime({
    url: '/location_geojson', 
    crossOrigin: true,
    type: 'json',
}, {
    interval: 1 * 1000,
    getFeatureId: function (feature) {
        return feature.properties.devicename;
    },
    pointToLayer: function (feature, latlng) {
        return L.marker(latlng, {icon: truckIcon});
    },
}).addTo(map);

var firstUpdate = true;

locationLayer.on('update', function(e) {
    Object.keys(e.features).forEach(function(key) {
        var feature = e.features[key];
        var layer = locationLayer.getLayer(key);
        layer.bindPopup('<h3>Accuracy: ' + feature.properties.accuracy + '</h3>Device:' + feature.properties.devicename);

        if (firstUpdate) {
            map.setView(layer.getLatLng(), 15);
            firstUpdate = false;
        }
    });
});
