import type * as L from 'leaflet';

// 遊び場オブジェクトの型を定義
interface Playground {
  id: string | number;
  name: string;
  address: string;
  phone: string;
  formatted_phone: string;
  latitude: string | number;
  longitude: string | number;
}

// windowオブジェクトにカスタムプロパティの型を定義
declare global {
  interface Window {
    mapInstance?: L.Map;
    favMapInstance?: L.Map;
    favorite_ids: string[];
    playgrounds: any[];
    L: typeof L;
  }
}

/**
 * マップ関連の機能（Leaflet.jsを使用）を管理するクラス。
 */
class MapManager {
  private L: typeof L;
  public readonly KAGOSHIMA_CENTER: L.LatLngTuple = [31.5602, 130.5581];
  public readonly DEFAULT_ZOOM_LEVEL: number = 10;

  /**
   * @param {L} [L_instance=window.L] - Leafletライブラリのインスタンス。
   */
  constructor(L_instance: typeof L = window.L) {
    this.L = L_instance;
  }

  /**
   * @param {Playground} playground - 遊び場の情報を含むオブジェクト。
   * @returns {string} ポップアップのHTML文字列。
   */
  createPopupContent(playground: Playground): string {
    const isFavorite = window.favorite_ids.includes(String(playground.id));
    const buttonText = isFavorite ? 'お気に入り解除' : 'お気に入りに追加';

    return `
      <div>
          <strong>${playground.name}</strong><br>
          住所: ${playground.address}<br>
          電話番号: ${playground.formatted_phone}<br>
          <a href="/facilities/${playground.id}/" class="btn btn-outline-primary btn-sm mt-2">詳細を見る</a>
          <button class="btn btn-outline-success btn-sm mt-2" data-playground-id="${playground.id}" data-action="toggle-favorite">
              ${buttonText}
          </button>
          <button class="btn btn-outline-secondary btn-sm mt-2" data-bs-toggle="modal" data-bs-target="#reviewModal"
                  data-playground-id="${playground.id}" data-playground-name="${playground.name}">
              口コミを書く
          </button>
          <a href="/playground/${playground.id}/reviews/" class="btn btn-outline-info btn-sm mt-2">口コミを見る</a>
      </div>
    `;
  }

  /**
   * @param {Playground[]} playgrounds - 遊び場の情報を含むオブジェクトの配列。
   */
  initMap(playgrounds: Playground[]): void {
    if (window.mapInstance) {
      window.mapInstance.remove();
    }

    window.mapInstance = this.L.map('map-container').setView(
      this.KAGOSHIMA_CENTER,
      this.DEFAULT_ZOOM_LEVEL
    );

    this.L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(window.mapInstance);

    playgrounds.forEach((playground) => {
      if (playground.latitude && playground.longitude) {
        const position: L.LatLngTuple = [
          parseFloat(playground.latitude as string),
          parseFloat(playground.longitude as string),
        ];
        const marker = this.L.marker(position).addTo(window.mapInstance!);
        marker.bindPopup(() => this.createPopupContent(playground));
      }
    });

    setTimeout(() => this.updateFavoriteButtonsOnMap(window.favorite_ids), 500);
  }

  /**
   * @param {Playground[]} playgrounds - お気に入り遊び場の情報を含むオブジェクトの配列。
   */
  initFavoritesMap(playgrounds: Playground[]): void {
    if (window.favMapInstance) {
      window.favMapInstance.remove();
    }

    const map = this.L.map('mypage-map-container').setView(
      this.KAGOSHIMA_CENTER,
      this.DEFAULT_ZOOM_LEVEL
    );
    window.favMapInstance = map;

    this.L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(map);

    playgrounds.forEach((playground) => {
      if (playground.latitude && playground.longitude) {
        const position: L.LatLngTuple = [
          parseFloat(playground.latitude as string),
          parseFloat(playground.longitude as string),
        ];
        const marker = this.L.marker(position).addTo(map);
        marker.bindPopup(() => this.createPopupContent(playground));
      }
    });
  }

  /**
   * @param {string[]} favorite_ids - お気に入り登録されている遊び場のIDの配列。
   */
  updateFavoriteButtonsOnMap(favorite_ids: string[]): void {
    document
      .querySelectorAll<HTMLButtonElement>('.btn-outline-success[data-playground-id]')
      .forEach((button) => {
        const playgroundId = button.getAttribute('data-playground-id');
        if (playgroundId) {
          const isFavorite = favorite_ids.includes(playgroundId);
          button.textContent = isFavorite ? 'お気に入り解除' : 'お気に入りに追加';
        }
      });
  }
}

export { MapManager };
