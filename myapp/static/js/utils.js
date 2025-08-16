/**
 * 指定された名前のクッキーの値を取得します。
 *
 * @param {string} name - 取得するクッキーの名前。
 * @returns {string|null} 指定された名前のクッキーの値。クッキーが存在しない場合はnull。
 */
export function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // このクッキー文字列が探している名前で始まるかチェック
      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
