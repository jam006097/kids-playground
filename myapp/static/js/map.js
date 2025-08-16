/**
 * マップ関連の機能（Leaflet.jsを使用）を管理するクラス。
 * マップの初期化、マーカーの追加、ポップアップコンテンツの生成、お気に入りボタンの更新などを行います。
 */
class MapManager {
  /**
   * MapManagerのコンストラクタ。
   * @param {object} [L_instance=L] - Leafletライブラリのインスタンス。テスト用にモックを注入できるようにします。
   */
  constructor(L_instance = L) {
    this.L = L_instance; // Leafletインスタンス
    this.KAGOSHIMA_CENTER = [31.5602, 130.5581]; // 鹿児島市の中心座標
    this.DEFAULT_ZOOM_LEVEL = 10; // デフォルトのズームレベル
  }

  /**
   * マーカーのポップアップに表示するHTMLコンテンツを生成します。
   * @param {object} playground - 遊び場の情報を含むオブジェクト。
   * @returns {string} ポップアップのHTML文字列。
   */
  createPopupContent(playground) {
    // 遊び場がお気に入りリストに含まれているかを確認
    const isFavorite = window.favorite_ids.includes(String(playground.id));
    // お気に入りボタンのテキストを決定
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
                <button class="btn btn-outline-secondary btn-sm mt-2" data-toggle="modal" data-target="#reviewModal"
                        data-playground-id="${playground.id}" data-playground-name="${playground.name}">
                    口コミを書く
                </button>
                <a href="/playground/${playground.id}/reviews/" class="btn btn-outline-info btn-sm mt-2">口コミを見る</a>
            </div>
        `;
  }

  /**
   * メインマップを初期化し、遊び場のマーカーを追加します。
   * @param {Array<object>} playgrounds - 遊び場の情報を含むオブジェクトの配列。
   */
  initMap(playgrounds) {
    // 既存のマップインスタンスがあれば削除
    if (window.mapInstance) {
      window.mapInstance.remove();
    }

    // 新しいマップインスタンスを作成し、指定された中心とズームレベルで表示
    window.mapInstance = this.L.map('map-container').setView(
      this.KAGOSHIMA_CENTER,
      this.DEFAULT_ZOOM_LEVEL,
    );

    // OpenStreetMapのタイルレイヤーを追加
    this.L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(window.mapInstance);

    // 各遊び場にマーカーを追加
    playgrounds.forEach((playground) => {
      if (playground.latitude && playground.longitude) {
        var position = [
          parseFloat(playground.latitude),
          parseFloat(playground.longitude),
        ];
        var marker = this.L.marker(position).addTo(window.mapInstance);
        // ポップアップコンテンツをバインド
        marker.bindPopup(() => this.createPopupContent(playground));
      }
    });

    // 500ミリ秒後にマップ上のお気に入りボタンを更新
    setTimeout(() => this.updateFavoriteButtonsOnMap(window.favorite_ids), 500);
  }

  /**
   * お気に入り遊び場用のマップを初期化し、マーカーを追加します。
   * initMapとほぼ同じですが、別のマップコンテナを使用します。
   * @param {Array<object>} playgrounds - お気に入り遊び場の情報を含むオブジェクトの配列。
   */
  initFavoritesMap(playgrounds) {
    // 既存のお気に入りマップインスタンスがあれば削除
    if (window.favMapInstance) {
      window.favMapInstance.remove();
    }

    // 新しいマップインスタンスを作成し、指定された中心とズームレベルで表示
    var map = this.L.map('mypage-map-container').setView(
      this.KAGOSHIMA_CENTER,
      this.DEFAULT_ZOOM_LEVEL,
    );
    window.favMapInstance = map;

    // OpenStreetMapのタイルレイヤーを追加
    this.L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(map);

    // 各遊び場にマーカーを追加
    playgrounds.forEach((playground) => {
      if (playground.latitude && playground.longitude) {
        var position = [
          parseFloat(playground.latitude),
          parseFloat(playground.longitude),
        ];
        var marker = this.L.marker(position).addTo(map);
        // ポップアップコンテンツをバインド
        marker.bindPopup(() => this.createPopupContent(playground));
      }
    });
  }

  /**
   * マップ上のお気に入りボタンのテキストを更新します。
   * @param {Array<string>} favorite_ids - お気に入り登録されている遊び場のIDの配列。
   */
  updateFavoriteButtonsOnMap(favorite_ids) {
    document
      .querySelectorAll('.btn-outline-success[data-playground-id]')
      .forEach((button) => {
        const playgroundId = button.getAttribute('data-playground-id');
        // ボタンの遊び場IDがお気に入りリストに含まれているか確認
        const isFavorite = favorite_ids.includes(playgroundId);
        // ボタンのテキストを更新
        button.textContent = isFavorite ? 'お気に入り解除' : 'お気に入りに追加';
      });
  }
}

export { MapManager };
