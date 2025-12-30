/**
 * @jest-environment node
 */
import { submitReview, Review } from '../review';

// global.fetch をテスト全体でモックする
global.fetch = jest.fn();
const mockedFetch = fetch as jest.Mock;

describe('Core Logic: submitReview', () => {
  let formData: FormData;

  // 各テストの前にモックとフォームデータを初期化
  beforeEach(() => {
    mockedFetch.mockClear();
    formData = new FormData();
    formData.append('rating', '5');
    formData.append('content', 'This is a test review.');
  });

  // 正常系のテスト
  describe('Given the submission is successful', () => {
    test('it should return the new review data when the API responds with success', async () => {
      // Given: APIが成功レスポンスを返すように設定
      const mockReview: Review = {
        user_account_name: 'Test User',
        rating: 5,
        content: 'This is a test review.',
        created_at: '2023-01-01 12:00',
      };
      mockedFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve({ status: 'success', review: mockReview }),
      } as Response);

      // When: submitReview を呼び出す
      const result = await submitReview('1', 'csrf-token', formData);

      // Then: 正しいエンドポイントにデータが送信され、レビューデータが返される
      expect(mockedFetch).toHaveBeenCalledWith('/playground/1/add_review/', {
        method: 'POST',
        headers: { 'X-CSRFToken': 'csrf-token' },
        body: formData,
      });
      expect(result).toEqual(mockReview);
    });
  });

  // 異常系のテスト
  describe('Given the submission has issues', () => {
    test('it should throw an error if playgroundId is not provided', async () => {
      // Given: playgroundId が空
      const playgroundId = '';
      // When/Then: submitReview を呼び出すとエラーがスローされる
      await expect(submitReview(playgroundId, 'csrf-token', formData)).rejects.toThrow(
        'Playground ID is not provided.',
      );
      expect(mockedFetch).not.toHaveBeenCalled();
    });

    test('it should throw an error if the network request fails', async () => {
      // Given: fetch がネットワークエラーで失敗するように設定
      const networkError = new Error('Network failure');
      mockedFetch.mockRejectedValueOnce(networkError);

      // When/Then: submitReview を呼び出すとエラーがスローされる
      await expect(submitReview('1', 'csrf-token', formData)).rejects.toThrow(networkError);
    });

    test('it should throw an error if the server responds with a non-ok status', async () => {
      // Given: APIサーバーが500エラーを返すように設定
      mockedFetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
      } as Response);

      // When/Then: submitReview を呼び出すとエラーがスローされる
      await expect(submitReview('1', 'csrf-token', formData)).rejects.toThrow(
        'Server responded with status: 500',
      );
    });

    test('it should throw an error if the API returns an application-level error', async () => {
      // Given: APIがアプリケーションレベルのエラーを返すように設定
      const errorMessage = 'Invalid input provided.';
      mockedFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve({ status: 'error', message: errorMessage }),
      } as Response);

      // When/Then: submitReview を呼び出すとエラーがスローされる
      await expect(submitReview('1', 'csrf-token', formData)).rejects.toThrow(errorMessage);
    });

    test('it should throw a generic error if the API response is malformed', async () => {
      // Given: APIが成功ステータスだが、期待されるデータを含まないレスポンスを返す
      mockedFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve({ status: 'success' }), // "review" プロパティが欠けている
      } as Response);

      // When/Then: submitReview を呼び出すとエラーがスローされる
      await expect(submitReview('1', 'csrf-token', formData)).rejects.toThrow(
        'An unknown error occurred.',
      );
    });
  });
});
