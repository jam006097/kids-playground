/**
 * Google Mapsを初期化し、地図上に子育て支援施設のマーカーを表示する関数。
 */
function initMap() {
    // 定数の定義
    const KAGOSHIMA_CENTER = {lat: 31.5602, lng: 130.5581};
    const DEFAULT_ZOOM_LEVEL = 14;
    const MIN_ZOOM_LEVEL_FOR_INFO_WINDOW = 13;

    // 地図の初期設定
    var mapOptions = {
        zoom: DEFAULT_ZOOM_LEVEL,
        center: KAGOSHIMA_CENTER  // デフォルトは鹿児島県の中心座標
    };

    var map = new google.maps.Map(document.getElementById('map'), mapOptions);

    // 位置情報の利用を許可するか確認
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var userLocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };

            // ユーザーの位置情報を中心に設定
            map.setCenter(userLocation);

            // ユーザーの位置が鹿児島県外の場合、鹿児島県の中心座標に戻す
            var geocoder = new google.maps.Geocoder();
            geocoder.geocode({'location': userLocation}, function(results, status) {
                if (status === 'OK') {
                    var addressComponents = results[0].address_components;
                    var isKagoshima = addressComponents.some(function(component) {
                        return component.long_name === '鹿児島県';
                    });

                    if (!isKagoshima) {
                        map.setCenter(KAGOSHIMA_CENTER);
                    }
                } else {
                    console.error('Geocode was not successful for the following reason: ' + status);
                }
            });
        }, function() {
            // 位置情報の利用を許可しない場合、鹿児島県の中心座標を使用
            handleLocationError(true, map, KAGOSHIMA_CENTER);
        });
    } else {
        // ブラウザが位置情報をサポートしていない場合、鹿児島県の中心座標を使用
        handleLocationError(false, map, KAGOSHIMA_CENTER);
    }

    // 各施設の住所をジオコーディングし、地図上にマーカーを追加
    var markers = [];
    playgrounds.forEach(function(playground) {
        var geocoder = new google.maps.Geocoder();
        geocoder.geocode({'address': playground.address}, function(results, status) {
            if (status === 'OK') {
                // マーカーを地図上に追加
                var marker = new google.maps.Marker({
                    map: map,
                    position: results[0].geometry.location,
                    title: playground.name
                });

                // 情報ウィンドウの内容を設定
                var infowindow = new google.maps.InfoWindow({
                    content: '<div><strong>' + playground.name + '</strong><br>' +
                             '<a href="#" onclick="searchOnGoogleMaps(\'' + playground.name + '\', \'' + playground.address + '\', \'' + playground.phone + '\')">Google Mapsで開く</a></div>',
                    disableAutoPan: true  // 情報ウィンドウを開いた際に表示位置が変更されないようにする
                });

                // 情報ウィンドウの状態を管理するフラグ
                var isInfoWindowOpen = true;

                // 情報ウィンドウを常に表示
                infowindow.open(map, marker);

                // 情報ウィンドウが閉じられたときのイベントリスナーを追加
                google.maps.event.addListener(infowindow, 'closeclick', function() {
                    isInfoWindowOpen = false;
                });

                // マーカーをクリックしたときに情報ウィンドウを表示
                marker.addListener('click', function() {
                    infowindow.open(map, marker);
                    isInfoWindowOpen = true;
                });

                markers.push({marker: marker, infowindow: infowindow, isInfoWindowOpen: isInfoWindowOpen});
            } else {
                console.error('Geocode was not successful for the following reason: ' + status);
                alert('Geocode was not successful for the following reason: ' + status);
            }
        });
    });

    // ズームレベルが変更されたときのイベントリスナーを追加
    map.addListener('zoom_changed', function() {
        var zoomLevel = map.getZoom();
        markers.forEach(function(item) {
            if (zoomLevel <= MIN_ZOOM_LEVEL_FOR_INFO_WINDOW) {
                item.infowindow.close();
            } else if (item.isInfoWindowOpen) {
                item.infowindow.open(map, item.marker);
            }
        });
    });
}

/**
 * 位置情報の取得に失敗した場合のエラーハンドリング関数。
 * @param {boolean} browserHasGeolocation - ブラウザが位置情報をサポートしているかどうか
 * @param {object} map - Google Mapsオブジェクト
 * @param {object} center - デフォルトの中心座標
 */
function handleLocationError(browserHasGeolocation, map, center) {
    console.error(browserHasGeolocation ?
                  'Error: The Geolocation service failed.' :
                  'Error: Your browser doesn\'t support geolocation.');
    map.setCenter(center);
}

/**
 * Google Mapsで施設を検索し、新しいタブで開く関数。
 * @param {string} name - 施設名
 * @param {string} address - 施設住所
 * @param {string} phone - 施設電話番号
 */
function searchOnGoogleMaps(name, address, phone) {
    // サーバーサイドのエンドポイントにリクエストを送信
    var searchUrl = `/search_place?name=${encodeURIComponent(name)}&address=${encodeURIComponent(address)}&phone=${encodeURIComponent(phone)}`;

    fetch(searchUrl)
        .then(response => response.json())
        .then(data => {
            if (data.url) {
                // 取得したURLを新しいタブで開く
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
