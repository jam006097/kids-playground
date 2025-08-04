const globals = require("globals");
const pluginPrettier = require("eslint-plugin-prettier");
const prettierRecommended = require("eslint-config-prettier");
const pluginJest = require("eslint-plugin-jest");

module.exports = [
  {
    languageOptions: {
      ecmaVersion: 12,
      sourceType: 'module',
      globals: {
        ...globals.browser,
        ...globals.node,
        ...globals.jest,
      },
    },
    plugins: {
      prettier: pluginPrettier,
      jest: pluginJest,
    },
    rules: {
      'no-unused-vars': 'warn',
      'no-console': 'off',
      'prettier/prettier': 'error',
    },
  },
  prettierRecommended, // eslint-config-prettier を直接追加
  {
    files: ['myapp/**/*.js'],
    rules: {
      // myapp 以下のJSファイルに適用されるルール
    },
  },
  {
    files: ['myapp/static/js/tests/**/*.js'],
    rules: {
      // Jest のテストファイルに適用されるルール
      'jest/no-disabled-tests': 'warn',
      'jest/no-focused-tests': 'error',
      'jest/no-identical-title': 'error',
      'jest/prefer-to-have-length': 'warn',
      'jest/valid-expect': 'error',
    },
  },
];
