module.exports = {
  testEnvironment: 'jsdom',
  // Ignore Python virtual environments to prevent module collisions
  modulePathIgnorePatterns: ['<rootDir>/venv/', '<rootDir>/venv_sync/'],
  transform: {
    '^.+\\.(js|ts)$': 'babel-jest',
  },
  moduleNameMapper: {
    '^leaflet$': '<rootDir>/__mocks__/leafletMock.js',
    '^../myapp/static/js/utils.js$': '<rootDir>/myapp/static/js/utils.js',
    '^@mapManager$': '<rootDir>/myapp/static/js/map.js',
  },
  testMatch: [
    '**/__tests__/**/*.js',
    '**/?(*.)+(spec|test).js',
    '**/myapp/static/js/tests/**/*.js',
    '**/tests/js/**/*.js',
    '**/myapp/static/js/tests/**/*.ts',
  ],
  moduleDirectories: ['node_modules', '<rootDir>'],
};
