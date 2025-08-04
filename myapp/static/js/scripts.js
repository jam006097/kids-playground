import { MapManager } from './map.js';
import { FavoriteManager } from './favorite.js';
import { ReviewManager } from './review.js';

document.addEventListener('DOMContentLoaded', function () {
  const mapManager = new MapManager();
  const favoriteManager = new FavoriteManager();
  const reviewManager = new ReviewManager();

  // ページに応じて適切な地図のイベントリスナーを設定
  if (document.getElementById('map-container')) {
    // トップページの地図処理
    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
      if (e.target.id === 'map-tab') {
        mapManager.initMap(window.playgrounds);
      }
    });
  } else if (document.getElementById('mypage-map-container')) {
    // お気に入りページの地図処理
    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
      if (e.target.id === 'map-tab') {
        mapManager.initFavoritesMap(window.playgrounds);
      }
    });
  }

  // ページ読み込み時にお気に入りボタンの状態を更新
  favoriteManager.updateFavoriteButtons(window.favorite_ids);

  // お気に入りボタンのイベントデリゲーション
  document.body.addEventListener('click', function (event) {
    const target = event.target;
    if (target.matches('[data-action="toggle-favorite"]')) {
      const playgroundId = target.getAttribute('data-playground-id');
      favoriteManager.toggleFavorite(target, playgroundId);
    }
  });

  // 口コミ関連のハンドラを初期化
  // ReviewManagerのコンストラクタでinitReviewHandlersが呼ばれるため、ここでは不要
  // reviewManager.initReviewHandlers();
});
