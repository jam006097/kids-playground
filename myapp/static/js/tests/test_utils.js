import { getCookie } from '../utils.js';

describe('getCookie', () => {
    test('クッキーが存在する場合、その値を正しく取得できること', () => {
        // Setup: テスト用のクッキーを設定
        document.cookie = "test_cookie=test_value";
        
        // Assertion: getCookieが正しい値を返すことを確認
        expect(getCookie('test_cookie')).toBe('test_value');
    });

    test('クッキーが存在しない場合、nullを返すこと', () => {
        // Assertion: 存在しないクッキー名を指定した場合、nullが返ることを確認
        expect(getCookie('non_existent_cookie')).toBeNull();
    });

    test('複数のクッキーが存在する場合、指定したクッキーの値を正しく取得できること', () => {
        // Setup: 複数のクッキーを設定
        document.cookie = "cookie1=value1";
        document.cookie = "cookie2=value2";
        document.cookie = "cookie3=value3";

        // Assertion: 2番目のクッキーの正しい値が返ることを確認
        expect(getCookie('cookie2')).toBe('value2');
    });

    test('値が空のクッキーの場合、空文字列を返すこと', () => {
        // Setup: 値が空のクッキーを設定
        document.cookie = "empty_cookie=";

        // Assertion: 空の文字列が返ることを確認
        expect(getCookie('empty_cookie')).toBe('');
    });
});