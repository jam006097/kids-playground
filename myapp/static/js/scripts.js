import { MapManager } from './map.js';
import { FavoriteManager } from './favorite.js';
import { ReviewManager } from './review.js';

document.addEventListener('DOMContentLoaded', function () {
  const mapManager = new MapManager();
  const favoriteManager = new FavoriteManager();
  // ReviewManagerを初期化
  const reviewModal = document.getElementById('reviewModal');
  const reviewForm = document.getElementById('reviewForm');
  if (reviewModal && reviewForm) {
    new ReviewManager(reviewModal, reviewForm);
  }

  // ページに応じて適切な地図のイベントリスナーを設定
  const mapTab = document.getElementById('map-tab');
  if (mapTab) {
    mapTab.addEventListener('shown.bs.tab', () => {
      if (document.getElementById('map-container')) {
        // トップページの地図処理
        mapManager.initMap(window.playgrounds);
      } else if (document.getElementById('mypage-map-container')) {
        // お気に入りページの地図処理
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
