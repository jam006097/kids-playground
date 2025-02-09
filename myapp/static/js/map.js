function initMap() {
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 10,
        center: {lat: 31.5602, lng: 130.5581}  // 鹿児島県の中心座標
    });

    playgrounds.forEach(function(playground) {
        var geocoder = new google.maps.Geocoder();
        geocoder.geocode({'address': playground.address}, function(results, status) {
            if (status === 'OK') {
                var marker = new google.maps.Marker({
                    map: map,
                    position: results[0].geometry.location,
                    title: playground.name
                });

                var infowindow = new google.maps.InfoWindow({
                    content: '<div><strong>' + playground.name + '</strong><br>' +
                             '住所: ' + playground.address + '<br>' +
                             '電話: ' + playground.phone + '</div>'
                });

                marker.addListener('click', function() {
                    infowindow.open(map, marker);
                });
            }
        });
    });
}
