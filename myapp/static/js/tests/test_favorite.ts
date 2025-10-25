import { FavoriteManager } from '../favorite';
import { getCookie } from '../utils.js'; // getCookieはutils.jsにあると仮定

// グローバルなfetch関数をモックする
global.fetch = jest.fn(() =>
  Promise.resolve({
    ok: true,
    json: () => Promise.resolve({ status: 'ok' }),
  })
) as jest.Mock;

describe('FavoriteManager', () => {
  let favoriteManager: FavoriteManager;
  let mockButton: HTMLButtonElement;

  beforeEach(() => {
    // 各テストの前にFavoriteManagerの新しいインスタンスを作成
    favoriteManager = new FavoriteManager(getCookie);
    // fetchのモックをクリア
    (fetch as jest.Mock).mockClear();
    // csrftokenをクッキーに設定
    document.cookie = 'csrftoken=mockcsrftoken';

    // 各テスト用にモックのボタン要素を作成
    mockButton = document.createElement('button');
    mockButton.dataset.playgroundId = '123';
    mockButton.textContent = 'お気に入りに追加'; // 初期状態: お気に入りではない
    mockButton.disabled = false;

    // エラーハンドリングテストのためにalertとconsole.errorをスパイ
    jest.spyOn(window, 'alert').mockImplementation(() => {});
    jest.spyOn(console, 'error').mockImplementation(() => {});

    // window.favorite_idsを初期化
    window.favorite_ids = [];
  });

  afterEach(() => {
    // 各テストの後にすべてのモックを復元
    jest.restoreAllMocks();
  });

  // シナリオ: お気に入りに追加する
  test('お気に入りに追加するリクエストを送信し、ボタンの表示を更新する', async () => {
    // 実行: toggleFavoriteを呼び出す
    await favoriteManager.toggleFavorite(mockButton, '123');

    // 検証: fetchが正しいURL、メソッド、ヘッダー、ボディで呼び出されたこと
    expect(fetch).toHaveBeenCalledWith('/add_favorite/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': 'mockcsrftoken',
      },
      body: 'playground_id=123',
    });
    // 検証: ボタンのテキストが「お気に入り解除」に更新されたこと
    expect(mockButton.textContent).toBe('お気に入り解除');
    // 検証: ボタンが無効化されていないこと
    expect(mockButton.disabled).toBe(false);
    // 検証: alertが呼び出されていないこと
    expect(window.alert).not.toHaveBeenCalled();
  });

  // シナリオ: お気に入りから削除する
  test('お気に入りから削除するリクエストを送信し、ボタンの表示を更新する', async () => {
    // 準備: ボタンの初期状態をお気に入り済みとする
    mockButton.textContent = 'お気に入り解除';

    // 実行: toggleFavoriteを呼び出す
    await favoriteManager.toggleFavorite(mockButton, '123');

    // 検証: fetchが正しいURL、メソッド、ヘッダー、ボディで呼び出されたこと
    expect(fetch).toHaveBeenCalledWith('/remove_favorite/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': 'mockcsrftoken',
      },
      body: 'playground_id=123',
    });
    // 検証: ボタンのテキストが「お気に入りに追加」に更新されたこと
    expect(mockButton.textContent).toBe('お気に入りに追加');
    // 検証: ボタンが無効化されていないこと
    expect(mockButton.disabled).toBe(false);
    // 検証: alertが呼び出されていないこと
    expect(window.alert).not.toHaveBeenCalled();
  });

  // シナリオ: window.favorite_idsが更新されることを確認する
  describe('window.favorite_idsの更新', () => {
    beforeEach(() => {
      // グローバルなwindow.favorite_idsを初期化
      window.favorite_ids = ['999']; // 既存のお気に入り
    });

    test('お気に入り追加時にwindow.favorite_idsにIDが追加される', async () => {
      // 実行
      await favoriteManager.toggleFavorite(mockButton, '123');
      // 検証
      expect(window.favorite_ids).toContain('123');
      expect(window.favorite_ids).toContain('999'); // 既存のIDが残っていること
    });

    test('お気に入り削除時にwindow.favorite_idsからIDが削除される', async () => {
      // 準備: ボタンとwindow.favorite_idsをお気に入り済みの状態にする
      mockButton.textContent = 'お気に入り解除';
      window.favorite_ids.push('123');

      // 実行
      await favoriteManager.toggleFavorite(mockButton, '123');
      // 検証
      expect(window.favorite_ids).not.toContain('123');
      expect(window.favorite_ids).toContain('999'); // 他のIDが残っていること
    });
  });

  // シナリオ: APIエラーが発生した場合
  test('APIエラーが発生した場合、アラートを表示する', async () => {
    // 準備: fetchがエラーレスポンスを返すようにモック
    (fetch as jest.Mock).mockImplementationOnce(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ status: 'error', message: 'API Error' }),
      })
    );

    // 実行: toggleFavoriteを呼び出す
    await favoriteManager.toggleFavorite(mockButton, '123');

    // 検証: 「操作に失敗しました。」というアラートが表示されたこと
    expect(window.alert).toHaveBeenCalledWith('操作に失敗しました。');
    // 検証: ボタンが無効化されていないこと
    expect(mockButton.disabled).toBe(false);
  });

  // シナリオ: ネットワークエラーが発生した場合
  test('ネットワークエラーが発生した場合、アラートを表示する', async () => {
    // 準備: fetchがネットワークエラーを発生させるようにモック
    (fetch as jest.Mock).mockImplementationOnce(() =>
      Promise.reject(new Error('Network Error'))
    );

    // 実行: toggleFavoriteを呼び出す
    await favoriteManager.toggleFavorite(mockButton, '123');

    // 検証: 「エラーが発生しました。」というアラートが表示されたこと
    expect(window.alert).toHaveBeenCalledWith('エラーが発生しました。');

    // 検証: ボタンが無効化されていないこと
    expect(mockButton.disabled).toBe(false);
  });

  // シナリオ: ボタンが無効化されている場合
  test('ボタンが無効化されている場合、処理を続行しない', async () => {
    // 準備: ボタンを無効化する
    mockButton.disabled = true;

    // 実行: toggleFavoriteを呼び出す
    await favoriteManager.toggleFavorite(mockButton, '123');

    // 検証: fetchが呼び出されていないこと
    expect(fetch).not.toHaveBeenCalled();
    // 検証: ボタンが無効化されたままであること
    expect(mockButton.disabled).toBe(true);
  });
});
