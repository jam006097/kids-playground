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
                    content: `
                    <div>
                        <strong>${playground.name}</strong><br>
                        住所: ${playground.address}<br>
                        電話番号: ${playground.phone}<br>
                        <button class="btn btn-outline-success btn-sm" data-playground-id="${playground.id}" onclick="toggleFavoriteFromMap('${playground.id}', this)">
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

                // domreadyイベントでお気に入りボタンの状態を更新する
                google.maps.event.addListener(infowindow, 'domready', function () {
                    updateFavoriteButtonsOnMap();
                });

                // 情報ウィンドウが閉じられたときのイベントリスナーを追加
                google.maps.event.addListener(infowindow, 'closeclick', function () {
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
    // 地図のマーカーがすべて描画された後にボタンの状態を更新
    setTimeout(updateFavoriteButtonsOnMap, 500);
}

/**
 * マイページタブ用にGoogle Mapsを初期化し、地図上にお気に入り施設のマーカーを表示する関数。
 */
function initFavoritesMap() {
    const KAGOSHIMA_CENTER = {lat: 31.5602, lng: 130.5581};
    const DEFAULT_ZOOM_LEVEL = 10;

    var mapOptions = {
        zoom: DEFAULT_ZOOM_LEVEL,
        center: KAGOSHIMA_CENTER
    };

    var map = new google.maps.Map(document.getElementById('mypage-map-container'), mapOptions);

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var userLocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };
            map.setCenter(userLocation);

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

    // お気に入り施設のマーカーとinfowindowを管理する配列（自動制御は行わない）
    var favMarkers = [];
    // テンプレートから渡される playgrounds_json を使用
    if (typeof playgrounds_json !== 'undefined' && playgrounds_json) {
        var favorites = JSON.parse(playgrounds_json);
        favorites.forEach(function(playground) {
            var geocoder = new google.maps.Geocoder();
            geocoder.geocode({'address': playground.address}, function(results, status) {
                if (status === 'OK') {
                    var marker = new google.maps.Marker({
                        map: map,
                        position: results[0].geometry.location,
                        title: playground.name
                    });
                    var infowindow = new google.maps.InfoWindow({
                        content: `
                        <div>
                            <strong>${playground.name}</strong><br>
                            住所: ${playground.address}<br>
                            電話番号: ${playground.phone}<br>
                            <button class="btn btn-outline-success btn-sm" data-playground-id="${playground.id}" onclick="toggleFavoriteFromFavorites(this, '${playground.id}')">
                                お気に入り解除
                            </button>
                            <button class="btn btn-outline-secondary btn-sm" data-toggle="modal" data-target="#reviewModal" data-playground-id="${playground.id}" data-playground-name="${playground.name}">
                                口コミを書く
                            </button>
                            <a href="/playground/${playground.id}/reviews/" class="btn btn-outline-info btn-sm">口コミを見る</a>
                        </div>
                        `,
                        disableAutoPan: true
                    });
                    // 初期表示時は infowindow を開かず、マーカークリック時にのみ表示する
                    marker.addListener('click', function() {
                        infowindow.open(map, marker);
                    });
                    favMarkers.push({marker: marker, infowindow: infowindow});
                } else {
                    console.error('Geocode error: ' + status);
                }
            });
        });
    }
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

// お気に入り情報を取得、保存、表示する関数を追加


function updateFavoritesDisplay() {
    // myapp/views/favorite_views.py から渡される playgrounds_json を使用
    // この変数はテンプレート内で定義されていることを想定
    if (typeof playgrounds_json !== 'undefined' && playgrounds_json) {
        var favorites = JSON.parse(playgrounds_json);
        var favoritesHtml = "";
        favorites.forEach(function(playground) {
            favoritesHtml += '<div class="col-md-4">';
            favoritesHtml += '  <div class="card mb-4 shadow-sm">';
            favoritesHtml += '    <div class="card-body">';
            favoritesHtml += '      <h5 class="card-title">' + playground.name + '</h5>';
            favoritesHtml += '      <p class="card-text">' + playground.address + '</p>';
            favoritesHtml += '      <p class="card-text">' + playground.phone + '</p>';
            // お気に入り切替ボタン（mypage用）
            favoritesHtml += '      <button class="btn btn-outline-success btn-sm" data-playground-id="' + playground.id + '" onclick="toggleFavoriteFromFavorites(this, \'' + playground.id + '\')">お気に入り解除</button>';
            // 口コミを書くボタン（モーダルを起動）
            favoritesHtml += '      <button class="btn btn-outline-secondary btn-sm" data-toggle="modal" data-target="#reviewModal" data-playground-id="' + playground.id + '" data-playground-name="' + playground.name + '">口コミを書く</button>';
            // 口コミを見るボタン
            favoritesHtml += '      <a href="/playground/' + playground.id + '/reviews/" class="btn btn-outline-info btn-sm">口コミを見る</a>';
            favoritesHtml += '    </div>';
            favoritesHtml += '  </div>';
            favoritesHtml += '</div>';
        });
        var container = document.querySelector("#mypage .row");
        if (container) {
            container.innerHTML = favoritesHtml;
        }
    }
}

// マイページ用：お気に入り切替処理（MyPageタブの施設詳細用）
function toggleFavoriteFromFavorites(button, playgroundId) {
    toggleFavorite(button, playgroundId);
}

// CSRFトークンを取得するヘルパー関数
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function toggleFavorite(button, playgroundId) {
    // ボタンが無効化されている場合は何もしない
    if (button.disabled) {
        return;
    }

    const csrfToken = getCookie('csrftoken');
    const isFavorite = button.textContent.includes('解除'); // 現在の状態をテキストで判断

    let url = '';
    if (isFavorite) {
        url = '/remove_favorite/';
    } else {
        url = '/add_favorite/';
    }

    // ボタンを無効化して二重クリックを防ぐ
    button.disabled = true;

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken,
        },
        body: `playground_id=${playgroundId}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'ok') {
            if (isFavorite) {
                button.textContent = 'お気に入りに追加';
            } else {
                button.textContent = 'お気に入り解除';
            }
            // お気に入り一覧ページにいる場合は、表示を更新
            if (window.location.pathname.includes('/favorites/')) {
                location.reload(); // ページをリロードして最新のお気に入り状態を反映
            }
        } else {
            alert('操作に失敗しました。');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('エラーが発生しました。');
    })
    .finally(() => {
        button.disabled = false; // ボタンを再度有効化
    });
}

function toggleFavoriteFromMap(playgroundId, button) {
    toggleFavorite(button, playgroundId);
}

function updateFavoriteButtonsOnMap() {
    // myapp/views/favorite_views.py から渡される favorite_ids を使用
    // この変数はテンプレート内で定義されていることを想定
    if (typeof favorite_ids !== 'undefined' && favorite_ids) {
        // 地図上のボタンを更新
        document.querySelectorAll('.btn-outline-success[data-playground-id]').forEach(function(button) {
            var playgroundId = button.getAttribute('data-playground-id');
            var isFavorite = favorite_ids.includes(playgroundId);

            if (isFavorite) {
                button.textContent = 'お気に入り解除';
            } else {
                button.textContent = 'お気に入りに追加';
            }
        });
    }
}

/**
 * お気に入りボタンの状態を更新する関数。
 */
function updateFavoriteButtons() {
    // myapp/views/favorite_views.py から渡される favorite_ids を使用
    // この変数はテンプレート内で定義されていることを想定
    if (typeof favorite_ids !== 'undefined' && favorite_ids) {
        // 一覧画面のボタンを更新
        document.querySelectorAll('.btn-outline-success[data-playground-id]').forEach(function(button) {
            var playgroundId = button.getAttribute('data-playground-id');
            var isFavorite = favorite_ids.includes(playgroundId);

            if (isFavorite) {
                button.textContent = 'お気に入り解除';
            } else {
                button.textContent = 'お気に入りに追加';
            }
        });
    }
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
    updateFavoriteButtons();
});

document.addEventListener("DOMContentLoaded", function () {
    // 地図タブがアクティブになったときにイベントリスナーを再登録
    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        if (e.target.id === 'map-tab') {
            initMap();
            updateFavoriteButtonsOnMap(); // 初期表示時にボタンの状態を更新

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

    // ページ読み込み時にお気に入り表示を更新
    updateFavoritesDisplay();
    updateFavoriteButtons();
    updateFavoriteButtonsOnMap(); // 初期表示時に地図上のボタンの状態を更新

});