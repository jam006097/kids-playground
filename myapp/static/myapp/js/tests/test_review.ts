/**
 * @jest-environment jsdom
 */

// モジュールのモックを先に設定
const mockModalHide = jest.fn();
const mockToastShow = jest.fn();

// グローバルなbootstrapオブジェクトをモック
window.bootstrap = {
  Modal: jest.fn().mockImplementation(() => ({
    hide: mockModalHide,
  })),
  Toast: jest.fn().mockImplementation(() => ({
    show: mockToastShow,
  })),
};

// fetchをグローバルにモック
global.fetch = jest.fn();

describe('Review Form Submission', () => {
  beforeEach(() => {
    // 各テストの前にDOMとモックをクリーンアップ
    document.body.innerHTML = `
      <div id="reviewModal"></div>
      <form id="reviewForm">
        <input type="hidden" name="csrfmiddlewaretoken" value="test-token">
        <input type="hidden" id="playgroundId" value="123">
        <input name="rating" id="rating">
        <textarea name="content" id="content"></textarea>
      </form>
      <ul id="review-list">
        <li id="no-reviews-message">まだ口コミがありません。</li>
      </ul>
      <div id="notificationToast" class="toast">
        <div id="notificationToastBody"></div>
      </div>
    `;

    // モジュールを動的にインポートして、DOMの準備ができた後にスクリプトが実行されるようにする
    require('../review.ts');

    // DOMContentLoadedを発火させて、スクリプト内のイベントリスナーを有効化
    document.dispatchEvent(
      new Event('DOMContentLoaded', {
        bubbles: true,
        cancelable: true,
      }),
    );

    // モックの呼び出し履歴をリセット
    (fetch as jest.Mock).mockClear();
    mockModalHide.mockClear();
    mockToastShow.mockClear();
    if (window.bootstrap.Modal) (window.bootstrap.Modal as jest.Mock).mockClear();
    if (window.bootstrap.Toast) (window.bootstrap.Toast as jest.Mock).mockClear();
  });

  test('should add review to the list on successful submission', async () => {
    // Arrange: 成功時のfetchレスポンスをモック
    const mockReview = {
      user_account_name: 'テストユーザー',
      rating: 5,
      content: '最高の公園でした！',
      created_at: '2023年01月01日 12:00',
    };
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ status: 'success', review: mockReview }),
    });

    const reviewForm = document.getElementById('reviewForm') as HTMLFormElement;
    const ratingInput = document.getElementById('rating') as HTMLInputElement;
    const contentInput = document.getElementById('content') as HTMLTextAreaElement;
    ratingInput.value = '5';
    contentInput.value = '最高の公園でした！';

    // Act: フォーム送信をシミュレート
    await reviewForm.dispatchEvent(new Event('submit'));

    // Assert: DOMの更新、モーダルの非表示、トーストの表示を確認
    const reviewList = document.getElementById('review-list') as HTMLUListElement;
    // 非同期処理の完了を待つ
    await new Promise(process.nextTick);

    expect(reviewList.querySelector('#no-reviews-message')).toBeNull();
    expect(reviewList.children.length).toBe(1);
    expect(reviewList.innerHTML).toContain('最高の公園でした！');
    expect(reviewList.innerHTML).toContain('テストユーザー');
    expect(ratingInput.value).toBe(''); // jest-environment-jsdomはreset()を完全にはサポートしないため、手動でチェック
    expect(contentInput.value).toBe('');
    expect(mockModalHide).toHaveBeenCalled();
    expect(mockToastShow).toHaveBeenCalled();
    expect(document.getElementById('notificationToastBody')?.textContent).toBe('口コミが投稿されました！');
  });

  test('should show an error toast on failed submission', async () => {
    // Arrange: 失敗時のfetchレスポンスをモック
    (fetch as jest.Mock).mockRejectedValueOnce(new Error('サーバーエラー'));

    const reviewForm = document.getElementById('reviewForm') as HTMLFormElement;

    // Act: フォーム送信をシミュレート
    await reviewForm.dispatchEvent(new Event('submit'));

    // Assert: エラートーストが表示され、DOMが変更されていないことを確認
    await new Promise(process.nextTick);

    const reviewList = document.getElementById('review-list') as HTMLUListElement;
    expect(reviewList.querySelector('#no-reviews-message')).not.toBeNull();
    expect(mockModalHide).not.toHaveBeenCalled();
    expect(mockToastShow).toHaveBeenCalled();
    expect(document.getElementById('notificationToastBody')?.textContent).toBe('サーバーエラー');
  });
});
