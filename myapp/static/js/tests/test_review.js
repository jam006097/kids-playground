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

describe('ReviewManager', () => {
  let reviewModal;
  let reviewForm;
  let playgroundIdInput;
  let modalTitle;
  let mockDocument;

  beforeEach(() => {
    fetch.mockClear();
    jest.spyOn(global, 'alert').mockImplementation(() => {});
    global.bootstrap.Modal.mockClear();
    mockBsModal.hide.mockClear();

    document.body.innerHTML = `
      <div class="modal" id="reviewModal">
        <h5 class="modal-title">口コミを投稿</h5>
        <form id="reviewForm">
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

    mockDocument = {
      querySelector: jest.fn((selector) => {
        if (selector === '[name=csrfmiddlewaretoken]') {
          return { value: 'mockCsrfToken' };
        }
        return document.querySelector(selector);
      }),
    };
  });

  afterEach(() => {
    document.body.innerHTML = '';
    jest.restoreAllMocks();
  });

  describe('jQueryからの脱却', () => {
    test('モーダル表示時に施設情報が設定されること', () => {
      const manager = new ReviewManager(reviewModal, reviewForm, mockDocument);

      const triggerButton = document.createElement('button');
      triggerButton.dataset.playgroundId = '456';
      triggerButton.dataset.playgroundName = '別の公園';

      const event = new Event('show.bs.modal');
      Object.defineProperty(event, 'relatedTarget', { value: triggerButton, writable: false });

      reviewModal.dispatchEvent(event);

      expect(playgroundIdInput.value).toBe('456');
      expect(modalTitle.textContent).toBe('別の公園への口コミ');
    });

    test('フォーム送信時にfetchが呼ばれ、成功時にモーダルが閉じること', async () => {
      const manager = new ReviewManager(reviewModal, reviewForm, mockDocument);
      playgroundIdInput.value = '123';

      // dispatchEventの代わりに、テスト対象のメソッドを直接呼び出す
      const mockEvent = { preventDefault: jest.fn() };
      await manager.handleSubmit(mockEvent);

      expect(fetch).toHaveBeenCalledWith(
        '/playground/123/add_review/',
        expect.objectContaining({
          method: 'POST',
          body: 'playground_id=123&rating=5&content=Great%21&csrfmiddlewaretoken=mockCsrfToken',
        })
      );
      expect(global.alert).toHaveBeenCalledWith('口コミが投稿されました。');
      expect(mockBsModal.hide).toHaveBeenCalled();
    });

    test('fetchリクエストが失敗した場合、alertが呼び出されること', async () => {
      fetch.mockRejectedValueOnce(new Error('Network error'));
      const manager = new ReviewManager(reviewModal, reviewForm, mockDocument);
      playgroundIdInput.value = '123';

      // dispatchEventの代わりに、テスト対象のメソッドを直接呼び出す
      const mockEvent = { preventDefault: jest.fn() };
      await manager.handleSubmit(mockEvent);

      expect(global.alert).toHaveBeenCalledWith('口コミの投稿に失敗しました。');
    });
  });
});
