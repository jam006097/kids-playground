import { MapManager } from './map.js';
import { FavoriteManager } from './favorite.js';
import { ReviewManager } from './review.js';

document.addEventListener('DOMContentLoaded', () => {
  const mapManager = new MapManager();
  const favoriteManager = new FavoriteManager();

  const reviewModal = document.getElementById('reviewModal') as HTMLElement;
  const reviewForm = document.getElementById('reviewForm') as HTMLFormElement;
  if (reviewModal && reviewForm) {
    new ReviewManager(reviewModal, reviewForm);
  }

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
