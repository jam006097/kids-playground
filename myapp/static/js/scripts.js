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

    var map = new google.maps.Map(document.getElementById('map-container'), mapOptions);

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
                    //content: '<div><strong>' + playground.name + '</strong><br>' +
                    //    '<a href="#" onclick="searchOnGoogleMaps(\'' + playground.name + '\', \'' + playground.address + '\', \'' + playground.phone + '\')">Google Mapsで開く</a></div>',
                    content: `
                    <div>
                        <strong>${playground.name}</strong><br>
                        住所: ${playground.address}<br>
                        電話番号: ${playground.phone}<br>
                        <button class="btn btn-outline-primary btn-sm" onclick="searchOnGoogleMaps('${playground.name}', '${playground.address}', '${playground.phone}')">
                            Google Mapsで開く
                        </button>
                        <button class="btn btn-outline-success btn-sm" onclick="toggleFavoriteFromMap('${playground.id}', this)">
                            お気に入りに追加
                        </button>
                        <button class="btn btn-outline-secondary btn-sm" data-toggle="modal" data-target="#reviewModal" 
                                data-playground-id="${playground.id}" data-playground-name="${playground.name}">
                            口コミを書く
                        </button>
                        <a href="/playground/${playground.id}/reviews/" class="btn btn-outline-info btn-sm">口コミを見る</a>
                    </div>
                `,
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
 * マイページタブ用にGoogle Mapsを初期化し、地図上にお気に入り施設のマーカーを表示する関数。
 */
function initFavoritesMap() {
    const KAGOSHIMA_CENTER = {lat: 31.5602, lng: 130.5581};
    const DEFAULT_ZOOM_LEVEL = 14;
    const MIN_ZOOM_LEVEL_FOR_INFO_WINDOW = 13;

    var mapOptions = {
        zoom: DEFAULT_ZOOM_LEVEL,
        center: KAGOSHIMA_CENTER
    };

    // マイページ用コンテナを指定
    var map = new google.maps.Map(document.getElementById('mypage-map-container'), mapOptions);

    // 位置情報の利用（initMapと同じ処理）
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var userLocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };

            // ユーザーの位置情報を中心に設定
            map.setCenter(userLocation);

            // 位置が鹿児島県外の場合、デフォルトの中心座標に戻す
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
            handleLocationError(true, map, KAGOSHIMA_CENTER);
        });
    } else {
        handleLocationError(false, map, KAGOSHIMA_CENTER);
    }

    // 各お気に入り施設の住所をジオコーディングし、地図上にマーカーを追加（お気に入りはローカルストレージから取得）
    var localFavorites = getLocalFavorites();
    localFavorites.forEach(function(playground) {
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
                             '<a href="#" onclick="searchOnGoogleMaps(\'' + playground.name + '\', \'' + playground.address + '\', \'' + playground.phone + '\')">Google Mapsで開く</a></div>',
                    disableAutoPan: true
                });
                infowindow.open(map, marker);
            } else {
                console.error('Geocode error: ' + status);
            }
        });
    });

    // ズームレベルが変更されたときの処理（必要に応じて追加）
    map.addListener('zoom_changed', function() {
        // ...existing code...
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

// お気に入り情報を取得、保存、表示する関数を追加
function getLocalFavorites() {
    var data = localStorage.getItem("favoriteFacilities");
    return data ? JSON.parse(data) : [];
}

function saveLocalFavorites(favorites) {
    localStorage.setItem("favoriteFacilities", JSON.stringify(favorites));
}

function updateFavoritesDisplay() {
    // MyPageタブ内のお気に入り一覧リストを更新する
    var favorites = getLocalFavorites();
    var favoritesHtml = "";
    favorites.forEach(function(playground) {
        favoritesHtml += '<div class="col-md-4">';
        favoritesHtml += '  <div class="card mb-4 shadow-sm">';
        favoritesHtml += '    <div class="card-body">';
        favoritesHtml += '      <h5 class="card-title">' + playground.name + '</h5>';
        favoritesHtml += '      <p class="card-text">' + playground.address + '</p>';
        favoritesHtml += '      <p class="card-text">' + playground.phone + '</p>';
        favoritesHtml += '      <a href="#" onclick="searchOnGoogleMaps(\'' + playground.name + '\', \'' + playground.address + '\', \'' + playground.phone + '\')">Google Mapsで開く</a>';
        favoritesHtml += '    </div>';
        favoritesHtml += '  </div>';
        favoritesHtml += '</div>';
    });
    var container = document.querySelector("#mypage .row");
    if (container) {
        container.innerHTML = favoritesHtml;
    }
}

function toggleFavorite(button, playgroundId) {
    // playgroundsは index.html で定義されている全施設の配列
    var facility = playgrounds.find(function(item) {
        return item.id.toString() === playgroundId.toString();
    });
    if (!facility) return;

    var favorites = getLocalFavorites();
    var foundIndex = favorites.findIndex(function(item) {
        return item.id.toString() === playgroundId.toString();
    });

    if (foundIndex !== -1) {
        // 既にお気に入りの場合、削除
        favorites.splice(foundIndex, 1);
        button.textContent = 'お気に入りに追加';
    } else {
        // お気に入りに追加（必要な項目を含める）
        var favItem = {
            id: facility.id,
            name: facility.name,
            address: facility.address,
            phone: facility.phone
        };
        favorites.push(favItem);
        button.textContent = 'お気に入り解除';
    }
    saveLocalFavorites(favorites);
    updateFavoritesDisplay();
}

function toggleFavoriteFromMap(playgroundId, button) {
    // playgrounds 配列から対象の施設を検索
    var facility = playgrounds.find(function(item) {
        return item.id.toString() === playgroundId.toString();
    });
    if (!facility) return;

    // ローカルストレージからお気に入りを取得
    var favorites = getLocalFavorites();
    var foundIndex = favorites.findIndex(function(item) {
        return item.id.toString() === playgroundId.toString();
    });

    if (foundIndex !== -1) {
        // 既にお気に入りの場合、削除
        favorites.splice(foundIndex, 1);
        button.textContent = 'お気に入りに追加';
    } else {
        // お気に入りに追加
        var favItem = {
            id: facility.id,
            name: facility.name,
            address: facility.address,
            phone: facility.phone
        };
        favorites.push(favItem);
        button.textContent = 'お気に入り解除';
    }

    // ローカルストレージに保存
    saveLocalFavorites(favorites);

    // お気に入り表示を更新
    updateFavoritesDisplay();
}

// タブがアクティブになった時に地図を初期化
$('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
    if (e.target.id === 'map-tab') {
        initMap();

        // 地図タブがアクティブになったときにイベントリスナーを再登録
        $('#reviewModal').on('show.bs.modal', function (event) {
            var button = $(event.relatedTarget); // ボタンを取得
            var playgroundId = button.data('playground-id');
            var playgroundName = button.data('playground-name');

            var modal = $(this);
            modal.find('#playgroundId').val(playgroundId);
            modal.find('.modal-title').text(playgroundName + 'への口コミ');
        });
    }
    if (e.target.id === 'mypage-tab') {
        initFavoritesMap();
    }
});

// ページ読み込み時にお気に入り表示を更新
document.addEventListener("DOMContentLoaded", function(){
    updateFavoritesDisplay();
});

document.addEventListener("DOMContentLoaded", function () {
    // 地図タブがアクティブになったときにイベントリスナーを再登録
    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        if (e.target.id === 'map-tab') {
            $('#reviewModal').on('show.bs.modal', function (event) {
                var button = $(event.relatedTarget); // ボタンを取得
                var playgroundId = button.data('playground-id');
                var playgroundName = button.data('playground-name');

                var modal = $(this);
                modal.find('#playgroundId').val(playgroundId);
                modal.find('.modal-title').text(playgroundName + 'への口コミ');
            });
        }
    });

    // モーダルが開かれるときに施設情報を設定
    $('#reviewModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget); // ボタンを取得
        var playgroundId = button.data('playground-id');
        var playgroundName = button.data('playground-name');

        var modal = $(this);
        modal.find('#playgroundId').val(playgroundId);
        modal.find('.modal-title').text(playgroundName + 'への口コミ');
    });

    // 口コミフォームの送信処理
    $('#reviewForm').on('submit', function (event) {
        event.preventDefault(); // デフォルトの送信を防止

        var formData = $(this).serialize(); // フォームデータを取得
        var playgroundId = $('#playgroundId').val();

        $.ajax({
            url: `/playground/${playgroundId}/add_review/`,
            method: 'POST',
            data: formData,
            success: function (response) {
                alert(response.message); // 成功メッセージを表示
                $('#reviewModal').modal('hide'); // モーダルを閉じる
            },
            error: function (xhr) {
                alert('口コミの投稿に失敗しました。');
            }
        });
    });
});