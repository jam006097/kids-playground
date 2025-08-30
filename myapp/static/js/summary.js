const ERROR_MESSAGE = '口コミの要約の取得に失敗しました。時間をおいて再度お試しください。';

/**
 * APIからAI要約を取得し、指定されたコンテナに結果を表示する。
 * @param {HTMLElement} container - 要約を表示するコンテナ要素。`data-url`属性を持つ必要がある。
 */
async function fetchSummary(container) {
    if (!container) {
        return;
    }

    const apiUrl = container.dataset.url;
    const summaryTextElement = container.querySelector('#summary-text');

    if (!apiUrl || !summaryTextElement) {
        summaryTextElement.textContent = '要約の表示に必要な情報を取得できませんでした。';
        return;
    }

    try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
            // サーバーがエラーを返した場合 (例: 400, 500)
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        summaryTextElement.textContent = data.summary || ERROR_MESSAGE;
    } catch (error) {
        // ネットワークエラーやJSONのパースエラーなど
        summaryTextElement.textContent = ERROR_MESSAGE;
    }
}

// DOMが読み込まれたら自動実行
document.addEventListener('DOMContentLoaded', () => {
    const summaryContainer = document.getElementById('summary-container');
    fetchSummary(summaryContainer);
});

// Jestでのテストのためにエクスポート
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { fetchSummary };
}
