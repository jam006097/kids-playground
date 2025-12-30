import { MapManager } from './map.js';
import { FavoriteManager } from './favorite.js';

// DOMからログイン状態を読み取る責務を持つ関数
const isAuthenticated = (): boolean => {
  return document.body.dataset.isAuthenticated === 'true';
};

document.addEventListener('DOMContentLoaded', () => {
  const mapManager = new MapManager();
  // FavoriteManagerに認証チェック関数を注入してインスタンス化
  const favoriteManager = new FavoriteManager(undefined, isAuthenticated);

  const mapTab = document.getElementById('map-tab');
  if (mapTab) {
    mapTab.addEventListener('shown.bs.tab', () => {
      if (document.getElementById('map-container')) {
        mapManager.initMap(window.playgrounds);
      } else if (document.getElementById('mypage-map-container')) {
        mapManager.initFavoritesMap(window.playgrounds);
      }
    });
  }

  if (window.favorite_ids) {
    favoriteManager.updateFavoriteButtons(window.favorite_ids);
  }

  document.body.addEventListener('click', (event) => {
    const target = event.target as HTMLElement;
    if (target && target.matches('[data-action="toggle-favorite"]')) {
      const playgroundId = target.getAttribute('data-playground-id');
      if (playgroundId) {
        favoriteManager.toggleFavorite(
          target as HTMLButtonElement,
          playgroundId,
        );
      }
    }
  });
});
