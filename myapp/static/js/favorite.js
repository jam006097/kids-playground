import { getCookie as defaultGetCookie } from './utils.js';

class FavoriteManager {
  constructor(getCookie = defaultGetCookie) {
    this.getCookie = getCookie;
  }

  toggleFavorite(button, playgroundId) {
    if (button.disabled) return;

    const csrfToken = this.getCookie('csrftoken');
    const isFavorite = button.textContent.includes('解除');
    const url = isFavorite ? '/remove_favorite/' : '/add_favorite/';

    button.disabled = true;

    return fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': csrfToken,
      },
      body: `playground_id=${playgroundId}`,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === 'ok') {
          button.textContent = isFavorite
            ? 'お気に入りに追加'
            : 'お気に入り解除';

          // 地図ポップアップ用のお気に入りIDリストを更新
          if (!isFavorite) {
            // お気に入りに追加
            window.favorite_ids.push(String(playgroundId));
          } else {
            // お気に入りから削除
            const index = window.favorite_ids.indexOf(String(playgroundId));
            if (index > -1) {
              window.favorite_ids.splice(index, 1);
            }
          }

          if (window.location.pathname.includes('/favorites/')) {
            location.reload();
          }
        } else {
          alert('操作に失敗しました。');
        }
      })
      .catch((error) => {
        console.error('フェッチエラー:', error);
        alert('エラーが発生しました。');
      })
      .finally(() => {
        button.disabled = false;
      });
  }

  updateFavoriteButtons(favorite_ids) {
    if (typeof favorite_ids !== 'undefined' && favorite_ids) {
      document
        .querySelectorAll('.btn-outline-success[data-playground-id]')
        .forEach((button) => {
          const playgroundId = button.getAttribute('data-playground-id');
          const isFavorite = favorite_ids.includes(playgroundId);
          button.textContent = isFavorite
            ? 'お気に入り解除'
            : 'お気に入りに追加';
        });
    }
  }
}

export { FavoriteManager };
