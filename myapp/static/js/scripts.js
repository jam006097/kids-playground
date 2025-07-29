/**
 * Leaflet.jsを使用して地図を初期化し、施設マーカーを表示する関数。
 */
function initMap() {
    const KAGOSHIMA_CENTER = [31.5602, 130.5581];
    const DEFAULT_ZOOM_LEVEL = 10;

    if (window.mapInstance) {
        window.mapInstance.remove();
    }

    window.mapInstance = L.map('map-container').setView(KAGOSHIMA_CENTER, DEFAULT_ZOOM_LEVEL);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(window.mapInstance);

    playgrounds.forEach(function(playground) {
        if (playground.latitude && playground.longitude) {
            var position = [parseFloat(playground.latitude), parseFloat(playground.longitude)];
            var marker = L.marker(position).addTo(window.mapInstance);
            var popupContent = `
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
            `;
            marker.bindPopup(popupContent);
        }
    });

    setTimeout(updateFavoriteButtonsOnMap, 500);
}

/**
 * Leaflet.jsを使用してお気に入り施設の地図を初期化する関数。
 */
function initFavoritesMap() {
    const KAGOSHIMA_CENTER = [31.5602, 130.5581];
    const DEFAULT_ZOOM_LEVEL = 10;

    if (window.favMapInstance) {
        window.favMapInstance.remove();
    }

    var map = L.map('mypage-map-container').setView(KAGOSHIMA_CENTER, DEFAULT_ZOOM_LEVEL);
    window.favMapInstance = map;

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    playgrounds.forEach(function(playground) {
        if (playground.latitude && playground.longitude) {
            var position = [parseFloat(playground.latitude), parseFloat(playground.longitude)];
            var marker = L.marker(position).addTo(map);
            var popupContent = `
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
            `;
            marker.bindPopup(popupContent);
        }
    });
}

function toggleFavoriteFromFavorites(button, playgroundId) {
    toggleFavorite(button, playgroundId);
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function toggleFavorite(button, playgroundId) {
    if (button.disabled) return;

    const csrfToken = getCookie('csrftoken');
    const isFavorite = button.textContent.includes('解除');
    const url = isFavorite ? '/remove_favorite/' : '/add_favorite/';

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
            button.textContent = isFavorite ? 'お気に入りに追加' : 'お気に入り解除';
            if (window.location.pathname.includes('/favorites/')) {
                location.reload();
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
        button.disabled = false;
    });
}

function toggleFavoriteFromMap(playgroundId, button) {
    toggleFavorite(button, playgroundId);
}

function updateFavoriteButtonsOnMap() {
    if (typeof favorite_ids !== 'undefined' && favorite_ids) {
        document.querySelectorAll('.btn-outline-success[data-playground-id]').forEach(function(button) {
            const playgroundId = button.getAttribute('data-playground-id');
            const isFavorite = favorite_ids.includes(playgroundId);
            button.textContent = isFavorite ? 'お気に入り解除' : 'お気に入りに追加';
        });
    }
}

function updateFavoriteButtons() {
    if (typeof favorite_ids !== 'undefined' && favorite_ids) {
        document.querySelectorAll('.btn-outline-success[data-playground-id]').forEach(function(button) {
            const playgroundId = button.getAttribute('data-playground-id');
            const isFavorite = favorite_ids.includes(playgroundId);
            button.textContent = isFavorite ? 'お気に入り解除' : 'お気に入りに追加';
        });
    }
}

document.addEventListener("DOMContentLoaded", function () {
    // ページに応じて適切な地図のイベントリスナーを設定
    if (document.getElementById('map-container')) {
        // トップページの地図処理
        $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
            if (e.target.id === 'map-tab') {
                initMap();
            }
        });
    } else if (document.getElementById('mypage-map-container')) {
        // お気に入りページの地図処理
        $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
            if (e.target.id === 'map-tab') {
                initFavoritesMap();
            }
        });
    }

    // モーダルが開かれるときに施設情報を設定
    $('#reviewModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var playgroundId = button.data('playground-id');
        var playgroundName = button.data('playground-name');
        var modal = $(this);
        modal.find('#playgroundId').val(playgroundId);
        modal.find('.modal-title').text(playgroundName + 'への口コミ');
    });

    // 口コミフォームの送信処理
    $('#reviewForm').on('submit', function (event) {
        event.preventDefault();
        var formData = $(this).serialize();
        var playgroundId = $('#playgroundId').val();
        $.ajax({
            url: `/playground/${playgroundId}/add_review/`,
            method: 'POST',
            data: formData,
            success: function (response) {
                alert(response.message);
                $('#reviewModal').modal('hide');
            },
            error: function (xhr) {
                alert('口コミの投稿に失敗しました。');
            }
        });
    });

    // ページ読み込み時にお気に入りボタンの状態を更新
    updateFavoriteButtons();
});
