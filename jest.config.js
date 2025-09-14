module.exports = {
  testEnvironment: 'jsdom',
  transform: {
    '^.+\.js$': 'babel-jest',
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
    '**/tests/js/**/*.js'
  ],
  moduleDirectories: ['node_modules', '<rootDir>'],
};
