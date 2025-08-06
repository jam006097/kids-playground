import { ReviewManager } from '../review.js';

describe('ReviewManager', () => {
  let mockJQuery;
  let mockAlert; // Still need this for mocking global alert

  let mockReviewModalElement;
  let mockReviewFormElement;
  let mockPlaygroundIdElement;
  let mockModalTitleElement; // Add this

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
    mockModalTitleElement = createMockElement(); // Initialize here
    mockModalTitleElement.text = jest.fn(); // Ensure text is a mock function

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
      if (selector === '.modal-title') return mockModalTitleElement; // Return the specific mock
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
    mockPlaygroundIdElement.val = jest.fn(() => '123'); // #playgroundIdのval()は常に'123'を返す

    // jQueryのモック
    mockJQuery = jest.fn((selector) => {
      // If the selector is the actual mockReviewModalElement object, return it directly
      if (selector === mockReviewModalElement) return mockReviewModalElement;
      if (selector === '#reviewModal') return mockReviewModalElement;
      if (selector === '#reviewForm') return mockReviewFormElement;
      if (selector === '#playgroundId') return mockPlaygroundIdElement; // This is for direct $(#playgroundId) calls
      // Generic mock for other selectors, including $(event.relatedTarget)
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

    // alertをモック
    mockAlert = jest.fn();
    global.alert = mockAlert; // Mock global alert

    // document.querySelectorをモック
    jest.spyOn(document, 'querySelector').mockImplementation((selector) => {
      if (selector === '[name=csrfmiddlewaretoken]') {
        return { value: 'mockCsrfToken' };
      }
      return null;
    });

    // ReviewManagerのインスタンスを作成する前にスパイを設定
    jest.spyOn(ReviewManager.prototype, 'initReviewHandlers');
    new ReviewManager(mockJQuery); // Remove mockAlert from constructor

    // Manually populate eventHandlers after initReviewHandlers is called
    // This is handled by the on mocks directly now
  });

  afterEach(() => {
    jest.clearAllMocks();
    jest.restoreAllMocks(); // スパイを元に戻す
  });

  test('constructorがinitReviewHandlersを呼び出すこと', () => {
    expect(ReviewManager.prototype.initReviewHandlers).toHaveBeenCalledTimes(1);
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
        currentTarget: mockReviewModalElement, // Add currentTarget for the modal element
      };

      showBsModalCallback.call(mockReviewModalElement, mockEvent);

      expect(mockReviewModalElement.find).toHaveBeenCalledWith('#playgroundId');
      expect(mockPlaygroundIdElement.val).toHaveBeenCalledWith('456');

      expect(mockReviewModalElement.find).toHaveBeenCalledWith('.modal-title');
      expect(mockModalTitleElement.text).toHaveBeenCalledWith(
        '別の公園への口コミ',
      );
    });
  });

  describe('initReviewHandlers - フォーム送信時の挙動', () => {
    beforeEach(() => {
      // Ensure $('#playgroundId').val() returns '123' for this test
      mockPlaygroundIdElement.val.mockReturnValue('123');
    });

    test('フォーム送信時にevent.preventDefaultが呼び出されること', () => {
      const mockEvent = {
        preventDefault: jest.fn(),
      };
      mockReviewFormElement.submitHandler(mockEvent);
      expect(mockEvent.preventDefault).toHaveBeenCalled();
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
      expect(global.alert).toHaveBeenCalledWith('口コミが投稿されました。'); // Use global.alert
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
      expect(global.alert).toHaveBeenCalledWith('口コミの投稿に失敗しました。'); // Use global.alert
    });
  });
});
