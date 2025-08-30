/**
 * @jest-environment jsdom
 */

// fetch関数をグローバルにモックする
global.fetch = jest.fn();

// テスト対象のモジュールをインポート
const { fetchSummary } = require('../summary');

document.body.innerHTML = `
    <div id="summary-container" data-playground-id="123" data-url="/summarize/playground/123/">
        <strong>AIによる口コミ要約:</strong>
        <div id="summary-text">
            <div class="d-flex align-items-center">
                <strong>要約を生成中...</strong>
                <div class="spinner-border ms-auto" role="status" aria-hidden="true"></div>
            </div>
        </div>
    </div>
`;

describe('fetchSummary', () => {
    const summaryContainer = document.getElementById('summary-container');
    const summaryText = document.getElementById('summary-text');

    beforeEach(() => {
        // 各テストの前にfetchモックをクリア
        fetch.mockClear();
        // DOMを初期状態に戻す
        summaryText.innerHTML = `
            <div class="d-flex align-items-center">
                <strong>要約を生成中...</strong>
                <div class="spinner-border ms-auto" role="status" aria-hidden="true"></div>
            </div>
        `;
    });

    test('APIが成功した場合、要約を表示すること', async () => {
        // 準備: fetchが成功レスポンスを返すように設定
        fetch.mockResolvedValueOnce({
            ok: true,
            json: async () => ({ summary: 'これがAIの要約です。' }),
        });

        // 実行
        await fetchSummary(summaryContainer);

        // 検証
        expect(fetch).toHaveBeenCalledTimes(1);
        expect(fetch).toHaveBeenCalledWith('/summarize/playground/123/');
        expect(summaryText.textContent).toBe('これがAIの要約です。');
    });

    test('APIがエラーを返した場合、エラーメッセージを表示すること', async () => {
        // 準備: fetchがエラーレスポンスを返すように設定
        fetch.mockResolvedValueOnce({
            ok: false,
            status: 500,
            json: async () => ({ error: 'サーバーエラー' }),
        });

        // 実行
        await fetchSummary(summaryContainer);

        // 検証
        expect(fetch).toHaveBeenCalledTimes(1);
        expect(summaryText.textContent).toContain('口コミの要約の取得に失敗しました');
    });

    test('ネットワークエラーが発生した場合、エラーメッセージを表示すること', async () => {
        // 準備: fetchがネットワークエラーを発生させるように設定
        fetch.mockRejectedValueOnce(new TypeError('Failed to fetch'));

        // 実行
        await fetchSummary(summaryContainer);

        // 検証
        expect(fetch).toHaveBeenCalledTimes(1);
        expect(summaryText.textContent).toContain('口コミの要約の取得に失敗しました');
    });

    test('コンテナ要素がない場合は何もしないこと', async () => {
        // 実行
        await fetchSummary(null);

        // 検証
        expect(fetch).not.toHaveBeenCalled();
    });
});
