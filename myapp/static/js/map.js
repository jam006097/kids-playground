class MapManager {
    constructor() {
        this.KAGOSHIMA_CENTER = [31.5602, 130.5581];
        this.DEFAULT_ZOOM_LEVEL = 10;
    }

    initMap(playgrounds) {
        if (window.mapInstance) {
            window.mapInstance.remove();
        }

        window.mapInstance = L.map('map-container').setView(this.KAGOSHIMA_CENTER, this.DEFAULT_ZOOM_LEVEL);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(window.mapInstance);

        playgrounds.forEach(playground => {
            if (playground.latitude && playground.longitude) {
                var position = [parseFloat(playground.latitude), parseFloat(playground.longitude)];
                var marker = L.marker(position).addTo(window.mapInstance);
                var popupContent = `
                    <div>
                        <strong>${playground.name}</strong><br>
                        住所: ${playground.address}<br>
                        電話番号: ${playground.phone}<br>
                        <button class="btn btn-outline-success btn-sm" data-playground-id="${playground.id}" data-action="toggle-favorite">
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

        setTimeout(() => this.updateFavoriteButtonsOnMap(window.favorite_ids), 500);
    }

    initFavoritesMap(playgrounds) {
        if (window.favMapInstance) {
            window.favMapInstance.remove();
        }

        var map = L.map('mypage-map-container').setView(this.KAGOSHIMA_CENTER, this.DEFAULT_ZOOM_LEVEL);
        window.favMapInstance = map;

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);

        playgrounds.forEach(playground => {
            if (playground.latitude && playground.longitude) {
                var position = [parseFloat(playground.latitude), parseFloat(playground.longitude)];
                var marker = L.marker(position).addTo(map);
                var popupContent = `
                    <div>
                        <strong>${playground.name}</strong><br>
                        住所: ${playground.address}<br>
                        電話番号: ${playground.phone}<br>
                        <button class="btn btn-outline-success btn-sm" data-playground-id="${playground.id}" data-action="toggle-favorite">
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

    updateFavoriteButtonsOnMap(favorite_ids) {
            document.querySelectorAll('.btn-outline-success[data-playground-id]').forEach(button => {
                const playgroundId = button.getAttribute('data-playground-id');
                const isFavorite = favorite_ids.includes(playgroundId);
                button.textContent = isFavorite ? 'お気に入り解除' : 'お気に入りに追加';
            });
        }
    }

export { MapManager };