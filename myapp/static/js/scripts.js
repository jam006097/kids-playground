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
                             '電話: ' + playground.phone + '<br>' +
                             '<a href="#" onclick="searchOnGoogleMaps(\'' + playground.name + '\', \'' + playground.address + '\', \'' + playground.phone + '\')">Google Mapsで開く</a></div>'
                });

                marker.addListener('click', function() {
                    infowindow.open(map, marker);
                });
            } else {
                console.error('Geocode was not successful for the following reason: ' + status);
                alert('Geocode was not successful for the following reason: ' + status);
            }
        });
    });
}

function searchOnGoogleMaps(name, address, phone) {
    var searchUrl = `/search_place?name=${encodeURIComponent(name)}&address=${encodeURIComponent(address)}&phone=${encodeURIComponent(phone)}`;

    fetch(searchUrl)
        .then(response => response.json())
        .then(data => {
            if (data.url) {
                window.open(data.url, '_blank');
            } else {
                console.error('No URL found in response');
                alert('No URL found in response');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error: ' + error);
        });
}
