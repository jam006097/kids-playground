import { ReviewManager } from '../review.js';

describe('ReviewManager', () => {
  let mockJQuery;
  let mockDocument;

  let mockReviewModalElement;
  let mockReviewFormElement;
  let mockPlaygroundIdElement;
  let mockModalTitleElement;

  // 各テストで新しいモック要素を作成するためのファクトリ関数
  const createMockElement = () => ({
    on: jest.fn(),
    val: jest.fn(),
    text: jest.fn(),
    serialize: jest.fn(() => 'formData'),
    modal: jest.fn(),
    find: jest.fn(() => createMockElement()), // findが新しいモック要素を返すように
    data: jest.fn(),
  });

  beforeEach(() => {
    // Specific mocks for #reviewModal, #reviewForm, and #playgroundId
    mockReviewModalElement = createMockElement();
    mockReviewFormElement = createMockElement();
    mockPlaygroundIdElement = createMockElement();
    mockModalTitleElement = createMockElement();
    mockModalTitleElement.text = jest.fn();

    // Override specific methods for these elements
    mockReviewModalElement.on = jest.fn((event, handler) => {
      if (event === 'show.bs.modal') {
        mockReviewModalElement.showBsModalHandler = handler;
      }
      return mockReviewModalElement;
    });
    mockReviewModalElement.modal = jest.fn();

    // mockReviewModalElementのfindメソッドを個別にモック
    mockReviewModalElement.find = jest.fn((selector) => {
      if (selector === '#playgroundId') return mockPlaygroundIdElement;
      if (selector === '.modal-title') return mockModalTitleElement;
      return createMockElement();
    });

    mockReviewFormElement.on = jest.fn((event, handler) => {
      if (event === 'submit') {
        mockReviewFormElement.submitHandler = handler;
      }
      return mockReviewFormElement;
    });
    mockReviewFormElement.serialize = jest.fn(() => 'formData');

    // Ensure mockPlaygroundIdElement.val is a mock function
    mockPlaygroundIdElement.val = jest.fn(() => '123');

    // jQueryのモック
    mockJQuery = jest.fn((selector) => {
      if (selector === mockReviewModalElement) return mockReviewModalElement;
      if (selector === '#reviewModal') return mockReviewModalElement;
      if (selector === '#reviewForm') return mockReviewFormElement;
      if (selector === '#playgroundId') return mockPlaygroundIdElement;
      const genericElement = createMockElement();
      genericElement.data = jest.fn((key) => {
        if (key === 'playground-id') return '456';
        if (key === 'playground-name') return '別の公園';
        return undefined;
      });
      return genericElement;
    });

    // $.ajaxをモック
    mockJQuery.ajax = jest.fn();
    global.$ = mockJQuery;

    // alertをスパイ
    jest.spyOn(global, 'alert').mockImplementation(() => {});

    // documentをモック
    mockDocument = {
      querySelector: jest.fn((selector) => {
        if (selector === '[name=csrfmiddlewaretoken]') {
          return { value: 'mockCsrfToken' };
        }
        return null;
      }),
    };

    // ReviewManagerのインスタンスを作成
    new ReviewManager(mockJQuery, mockDocument);
  });

  afterEach(() => {
    jest.clearAllMocks();
    jest.restoreAllMocks();
  });

  describe('initReviewHandlers - モーダル表示時の挙動', () => {
    test('モーダルが開かれたときに施設情報が正しく設定されること', () => {
      const showBsModalCallback = mockReviewModalElement.showBsModalHandler;

      const mockEvent = {
        relatedTarget: {
          dataset: {
            'playground-id': '456',
            'playground-name': '別の公園',
          },
        },
        currentTarget: mockReviewModalElement,
      };

      showBsModalCallback.call(mockReviewModalElement, mockEvent);

      expect(mockPlaygroundIdElement.val).toHaveBeenCalledWith('456');
      expect(mockModalTitleElement.text).toHaveBeenCalledWith(
        '別の公園への口コミ',
      );
    });
  });

  describe('initReviewHandlers - フォーム送信時の挙動', () => {
    beforeEach(() => {
      mockPlaygroundIdElement.val.mockReturnValue('123');
    });

    test('AJAXリクエストが成功した場合、alertが呼び出されモーダルが閉じられること', async () => {
      mockJQuery.ajax.mockImplementationOnce((options) => {
        options.success({
          message: '口コミが投稿されました。',
        });
      });

      const mockEvent = {
        preventDefault: jest.fn(),
      };
      mockReviewFormElement.submitHandler(mockEvent);

      expect(mockJQuery.ajax).toHaveBeenCalledWith(
        expect.objectContaining({
          url: '/playground/123/add_review/',
          method: 'POST',
          data: 'formData&csrfmiddlewaretoken=mockCsrfToken',
        }),
      );
      expect(global.alert).toHaveBeenCalledWith('口コミが投稿されました。');
      expect(mockReviewModalElement.modal).toHaveBeenCalledWith('hide');
    });

    test('AJAXリクエストが失敗した場合、alertが呼び出されること', async () => {
      mockJQuery.ajax.mockImplementationOnce((options) => {
        options.error({});
      });

      const mockEvent = {
        preventDefault: jest.fn(),
      };
      mockReviewFormElement.submitHandler(mockEvent);

      expect(mockJQuery.ajax).toHaveBeenCalledWith(
        expect.objectContaining({
          url: '/playground/123/add_review/',
          method: 'POST',
          data: 'formData&csrfmiddlewaretoken=mockCsrfToken',
        }),
      );
      expect(global.alert).toHaveBeenCalledWith('口コミの投稿に失敗しました。');
    });
  });
});