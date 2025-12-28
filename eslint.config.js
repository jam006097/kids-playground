const globals = require("globals");
const pluginPrettier = require("eslint-plugin-prettier");
const prettierRecommended = require("eslint-config-prettier");
const pluginJest = require("eslint-plugin-jest");
const tsEslint = require("@typescript-eslint/eslint-plugin");
const tsParser = require("@typescript-eslint/parser");

module.exports = [
  prettierRecommended, // Make sure this is last -> moved to top
  {
    // General configuration for all files
    plugins: {
      prettier: pluginPrettier,
    },
    rules: {
      'prettier/prettier': 'error',
    },
  },
  {
    // Configuration for TypeScript files
    files: ["myapp/**/*.ts"],
    languageOptions: {
      parser: tsParser,
      parserOptions: {
        ecmaVersion: 12,
        sourceType: 'module',
      },
      globals: {
        ...globals.browser,
        ...globals.node,
      },
    },
    plugins: {
      '@typescript-eslint': tsEslint,
    },
    rules: {
      ...tsEslint.configs['recommended'].rules,
      '@typescript-eslint/no-explicit-any': 'warn',
      '@typescript-eslint/no-unused-vars': [
        'warn',
        {
          argsIgnorePattern: '^_',
          varsIgnorePattern: '^_',
          caughtErrorsIgnorePattern: '^_',
        },
      ],
      'no-unused-vars': 'off', // Turn off base rule to avoid conflicts
      'no-console': 'off',
    },
  },
  {
    // Configuration for Jest test files (TypeScript)
    files: ["myapp/static/js/tests/**/*.ts"],
    languageOptions: {
        globals: {
            ...globals.jest,
        },
    },
    plugins: {
      jest: pluginJest,
    },
    rules: {
      ...pluginJest.configs.recommended.rules,
      'jest/no-disabled-tests': 'warn',
      'jest/no-focused-tests': 'error',
      'jest/no-identical-title': 'error',
      'jest/prefer-to-have-length': 'warn',
      'jest/valid-expect': 'error',
    },
  },
  {
    // Override for test_map.ts to allow any, because disable comments are not working.
    files: ["myapp/static/js/tests/test_map.ts"],
    rules: {
      '@typescript-eslint/no-explicit-any': 'off',
    },
  },
];
