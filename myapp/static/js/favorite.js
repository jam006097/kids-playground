import { getCookie as defaultGetCookie } from './utils.js';

/**
 * お気に入り機能の管理を行うクラス。
 * お気に入り状態の切り替え、ボタンの表示更新、CSRFトークンの取得などを担当します。
 */
class FavoriteManager {
  /**
   * FavoriteManagerのコンストラクタ。
   * @param {function} [getCookie=defaultGetCookie] - クッキーを取得するための関数。テスト用にモックを注入できるようにします。
   */
  constructor(getCookie = defaultGetCookie) {
    this.getCookie = getCookie;
  }

  /**
   * 遊び場のお気に入り状態を切り替えます。
   * サーバーへのPOSTリクエストを送信し、成功した場合にボタンのテキストとお気に入りIDリストを更新します。
   * @param {HTMLElement} button - お気に入りボタンのDOM要素。
   * @param {string} playgroundId - 遊び場のID。
   * @returns {Promise<void>} 非同期操作のPromise。
   */
  toggleFavorite(button, playgroundId) {
    // ボタンが無効化されている場合は処理を中断
    if (button.disabled) return;

    const csrfToken = this.getCookie('csrftoken'); // CSRFトークンを取得
    // ボタンのテキストから現在のお気に入り状態を判断
    const isFavorite = button.textContent.includes('解除');
    // お気に入り状態に応じてリクエストURLを決定
    const url = isFavorite ? '/remove_favorite/' : '/add_favorite/';

    button.disabled = true; // ボタンを無効化して二重クリックを防止

    // fetch APIを使用してサーバーにリクエストを送信
    return fetch(url, {
      method: 'POST', // POSTメソッドを使用
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': csrfToken,
      },
      body: `playground_id=${playgroundId}`,
    })
      .then((response) => response.json()) // レスポンスをJSONとしてパース
      .then((data) => {
        if (data.status === 'ok') {
          // サーバーからの応答が成功の場合
          // ボタンのテキストを新しいお気に入り状態に合わせて更新
          button.textContent = isFavorite
            ? 'お気に入りに追加'
            : 'お気に入り解除';

          // 地図ポップアップ用のお気に入りIDリスト (window.favorite_ids) を更新
          if (!isFavorite) {
            // お気に入りに追加された場合
            window.favorite_ids.push(String(playgroundId));
          } else {
            // お気に入りから削除された場合
            const index = window.favorite_ids.indexOf(String(playgroundId));
            if (index > -1) {
              window.favorite_ids.splice(index, 1); // リストからIDを削除
            }
          }

          // 現在のページがお気に入りページの場合、ページをリロードして表示を更新
          if (window.location.pathname.includes('/favorites/')) {
            location.reload();
          }
        } else {
          // サーバーからの応答が失敗の場合
          alert('操作に失敗しました。');
        }
      })
      .catch((error) => {
        // フェッチエラーが発生した場合
        console.error('フェッチエラー:', error);
        alert('エラーが発生しました。');
      })
      .finally(() => {
        // リクエスト完了後にボタンを有効化
        button.disabled = false;
      });
  }

  /**
   * ページ上のお気に入りボタンのテキストを、指定されたお気に入りIDリストに基づいて更新します。
   * @param {Array<string>} favorite_ids - お気に入り登録されている遊び場のIDの配列。
   */
  updateFavoriteButtons(favorite_ids) {
    // favorite_idsが定義されており、かつnullやundefinedでないことを確認
    if (typeof favorite_ids !== 'undefined' && favorite_ids) {
      // data-playground-id属性を持つすべてのお気に入りボタン要素を取得
      document
        .querySelectorAll('.btn-outline-success[data-playground-id]')
        .forEach((button) => {
          const playgroundId = button.getAttribute('data-playground-id'); // ボタンから遊び場IDを取得
          // ボタンの遊び場IDがお気に入りリストに含まれているか確認
          const isFavorite = favorite_ids.includes(playgroundId);
          // ボタンのテキストを更新
          button.textContent = isFavorite
            ? 'お気に入り解除'
            : 'お気に入りに追加';
        });
    }
  }
}

export { FavoriteManager };
