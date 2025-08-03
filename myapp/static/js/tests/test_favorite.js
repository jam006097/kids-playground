import { FavoriteManager } from '../favorite.js';
import { getCookie } from '../utils.js'; // Assuming getCookie is in utils.js

// Mock the global fetch function
global.fetch = jest.fn(() =>
    Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ status: 'ok' }),
    })
);

// Mock getCookie function
jest.mock('../utils.js', () => ({
    getCookie: jest.fn(() => 'mockcsrftoken'),
}));

describe('FavoriteManager', () => {
    let favoriteManager;
    let mockButton;

    beforeEach(() => {
        favoriteManager = new FavoriteManager();
        fetch.mockClear();
        getCookie.mockClear();

        // Create a mock button element for each test
        mockButton = document.createElement('button');
        mockButton.dataset.playgroundId = '123';
        mockButton.textContent = 'お気に入りに追加'; // Default state: not favorited
        mockButton.disabled = false;

        // Mock alert for error handling tests
        jest.spyOn(window, 'alert').mockImplementation(() => {});
        jest.spyOn(console, 'error').mockImplementation(() => {});
    });

    afterEach(() => {
        jest.restoreAllMocks();
    });

    // Test case for adding to favorites
    test('should send POST request to add_favorite and update button text', async () => {
        await favoriteManager.toggleFavorite(mockButton, '123');

        expect(getCookie).toHaveBeenCalledWith('csrftoken');
        expect(fetch).toHaveBeenCalledWith('/add_favorite/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': 'mockcsrftoken',
            },
            body: 'playground_id=123',
        });
        expect(mockButton.textContent).toBe('お気に入り解除');
        expect(mockButton.disabled).toBe(false);
        expect(window.alert).not.toHaveBeenCalled();
    });

    // Test case for removing from favorites
    test('should send POST request to remove_favorite and update button text', async () => {
        mockButton.textContent = 'お気に入り解除'; // Set initial state to favorited

        await favoriteManager.toggleFavorite(mockButton, '123');

        expect(getCookie).toHaveBeenCalledWith('csrftoken');
        expect(fetch).toHaveBeenCalledWith('/remove_favorite/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': 'mockcsrftoken',
            },
            body: 'playground_id=123',
        });
        expect(mockButton.textContent).toBe('お気に入りに追加');
        expect(mockButton.disabled).toBe(false);
        expect(window.alert).not.toHaveBeenCalled();
    });

    // Test case for API error
    test('should alert on API error', async () => {
        fetch.mockImplementationOnce(() =>
            Promise.resolve({
                ok: true,
                json: () => Promise.resolve({ status: 'error', message: 'API Error' }),
            })
        );

        await favoriteManager.toggleFavorite(mockButton, '123');

        expect(window.alert).toHaveBeenCalledWith('操作に失敗しました。');
        expect(console.error).toHaveBeenCalledWith('APIからのエラー:', 'API Error');
        expect(mockButton.disabled).toBe(false);
    });

    // Test case for network error
    test('should alert on network error', async () => {
        fetch.mockImplementationOnce(() => Promise.reject(new Error('Network Error')));

        await favoriteManager.toggleFavorite(mockButton, '123');

        expect(window.alert).toHaveBeenCalledWith('エラーが発生しました。');
        expect(console.error).toHaveBeenCalledWith('フェッチエラー:', expect.any(Error));
        expect(mockButton.disabled).toBe(false);
    });

    // Test case for button disabled state
    test('should not proceed if button is disabled', async () => {
        mockButton.disabled = true;

        await favoriteManager.toggleFavorite(mockButton, '123');

        expect(fetch).not.toHaveBeenCalled();
        expect(mockButton.disabled).toBe(true);
    });
});