const mockJQuery = jest.fn((selector) => {
    // Simulate jQuery chaining
    return {
        on: jest.fn().mockReturnThis(),
        find: jest.fn().mockReturnThis(),
        val: jest.fn().mockReturnThis(),
        text: jest.fn().mockReturnThis(),
        data: jest.fn((key) => {
            if (key === 'playground-id') return '123';
            if (key === 'playground-name') return 'Test Playground';
            return undefined;
        }),
        // Add other jQuery methods as needed for tests
    };
});

module.exports = mockJQuery;