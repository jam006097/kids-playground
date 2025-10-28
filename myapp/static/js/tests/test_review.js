import { ReviewManager } from '../review.js';

// Bootstrap 5 Modalのモック
const mockBsModal = {
  hide: jest.fn(),
};
if (typeof global.bootstrap === 'undefined') {
  global.bootstrap = {};
}
global.bootstrap.Modal = jest.fn(() => mockBsModal);

// fetchをグローバルにモック
global.fetch = jest.fn(() =>
  Promise.resolve({
    ok: true,
    json: () => Promise.resolve({ message: '口コミが投稿されました。' }),
  })
);

describe('ReviewManagerの口コミ投稿機能', () => {
  let reviewModal;
  let reviewForm;
  let playgroundIdInput;
  let modalTitle;

  beforeEach(() => {
    fetch.mockClear();
    jest.spyOn(global, 'alert').mockImplementation(() => {});
    global.bootstrap.Modal.mockClear();
    mockBsModal.hide.mockClear();

    // テスト用のDOMに、CSRFトークンを含んだフォームをセットアップ
    document.body.innerHTML = `
      <div class="modal" id="reviewModal">
        <h5 class="modal-title">口コミを投稿</h5>
        <form id="reviewForm">
          <input type="hidden" name="csrfmiddlewaretoken" value="mockCsrfToken">
          <input type="hidden" id="playgroundId" name="playground_id">
          <input name="rating" value="5">
          <textarea name="content">Great!</textarea>
        </form>
      </div>
    `;

    reviewModal = document.getElementById('reviewModal');
    reviewForm = document.getElementById('reviewForm');
    playgroundIdInput = document.getElementById('playgroundId');
    modalTitle = reviewModal.querySelector('.modal-title');
  });

  afterEach(() => {
    document.body.innerHTML = '';
    jest.restoreAllMocks();
  });

  test('「口コミを書く」ボタンでモーダルを開いたとき、対象の施設名がタイトルに表示されること', () => {
    // managerのコンストラクタには本物のdocumentを渡す
    const manager = new ReviewManager(reviewModal, reviewForm, document);

    const triggerButton = document.createElement('button');
    triggerButton.dataset.playgroundId = '456';
    triggerButton.dataset.playgroundName = '別の公園';

    const event = new Event('show.bs.modal');
    Object.defineProperty(event, 'relatedTarget', { value: triggerButton, writable: false });

    reviewModal.dispatchEvent(event);

    expect(playgroundIdInput.value).toBe('456');
    expect(modalTitle.textContent).toBe('別の公園への口コミ');
  });

  test('有効な口コミを送信したとき、「投稿しました」と表示されモーダルが閉じること', async () => {
    const manager = new ReviewManager(reviewModal, reviewForm, document);
    playgroundIdInput.value = '123';

    const mockEvent = { preventDefault: jest.fn() };
    await manager.handleSubmit(mockEvent);

    // 検証：ユーザーに観測可能な振る舞いのみをテストする
    expect(global.alert).toHaveBeenCalledWith('口コミが投稿されました。');
    expect(mockBsModal.hide).toHaveBeenCalled();
  });

  test('口コミの送信に失敗したとき、「投稿に失敗しました」と表示されること', async () => {
    fetch.mockRejectedValueOnce(new Error('Network error'));
    const manager = new ReviewManager(reviewModal, reviewForm, document);
    playgroundIdInput.value = '123';

    const mockEvent = { preventDefault: jest.fn() };
    await manager.handleSubmit(mockEvent);

    expect(global.alert).toHaveBeenCalledWith('口コミの投稿に失敗しました。');
  });
});
