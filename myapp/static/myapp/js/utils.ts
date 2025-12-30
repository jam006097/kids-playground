export function getCookie(name: string): string | null {
  let cookieValue: string | null = null;
  if (document.cookie && document.cookie !== '') {
    const cookies: string[] = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie: string = cookies[i].trim();
      // このクッキー文字列が探している名前で始まるかチェック
      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
