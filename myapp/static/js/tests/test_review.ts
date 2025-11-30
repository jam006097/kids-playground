import { ReviewManager } from '../review';

// jest.config.jsのmoduleNameMapperにより、'bootstrap'はダミーに置き換えられるが、
// テストコード内でbootstrap.Modalがコンストラクタとして振る舞うように、ここで再度モックする。
const mockHide = jest.fn();
const mockModalConstructor = jest.fn(() => ({
  hide: mockHide,
}));

// fetchをグローバルにモック
global.fetch = jest.fn(() =>
  Promise.resolve({
    ok: true,
    json: () => Promise.resolve({ message: '口コミが投稿されました。' }),
  }),
) as jest.Mock;

describe('ReviewManagerの口コミ投稿機能', () => {
  let reviewModal: HTMLElement;
  let reviewForm: HTMLFormElement;
  let playgroundIdInput: HTMLInputElement;
  let modalTitle: HTMLElement;

  beforeEach(() => {
    // グローバルなwindowオブジェクトにbootstrapのモックをセットアップ
    (window as any).bootstrap = {
      Modal: mockModalConstructor,
    };

    // 各モックをクリア
    (fetch as jest.Mock).mockClear();
    mockModalConstructor.mockClear();
    mockHide.mockClear();
    jest.spyOn(global, 'alert').mockImplementation(() => {});

    // テスト用のDOMをセットアップ
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

    reviewModal = document.getElementById('reviewModal')!;
    reviewForm = document.getElementById('reviewForm')! as HTMLFormElement;
    playgroundIdInput = document.getElementById(
      'playgroundId',
    )! as HTMLInputElement;
    modalTitle = reviewModal.querySelector('.modal-title')!;
  });

  afterEach(() => {
    document.body.innerHTML = '';
    jest.restoreAllMocks();
  });

  test('「口コミを書く」ボタンでモーダルを開いたとき、対象の施設名がタイトルに表示されること', () => {
    const manager = new ReviewManager(reviewModal, reviewForm, document);
    const triggerButton = document.createElement('button');
    triggerButton.dataset.playgroundId = '456';
    triggerButton.dataset.playgroundName = '別の公園';

    const event = new Event('show.bs.modal');
    Object.defineProperty(event, 'relatedTarget', {
      value: triggerButton,
      writable: false,
    });

    reviewModal.dispatchEvent(event);

    expect(playgroundIdInput.value).toBe('456');
    expect(modalTitle.textContent).toBe('別の公園への口コミ');
  });

  test('有効な口コミを送信したとき、「投稿しました」と表示されモーダルが閉じること', async () => {
    const manager = new ReviewManager(reviewModal, reviewForm, document);
    playgroundIdInput.value = '123';

    const mockEvent = { preventDefault: jest.fn() };
    await manager.handleSubmit(mockEvent as Event);

    expect(global.alert).toHaveBeenCalledWith('口コミが投稿されました。');
    expect(mockHide).toHaveBeenCalled();
  });

  test('口コミの送信に失敗したとき、「投稿に失敗しました」と表示されること', async () => {
    (fetch as jest.Mock).mockRejectedValueOnce(new Error('Network error'));
    const manager = new ReviewManager(reviewModal, reviewForm, document);
    playgroundIdInput.value = '123';

    const mockEvent = { preventDefault: jest.fn() };
    await manager.handleSubmit(mockEvent as Event);

    expect(global.alert).toHaveBeenCalledWith('口コミの投稿に失敗しました。');
  });
});
