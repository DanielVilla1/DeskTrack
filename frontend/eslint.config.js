import js from "@eslint/js";
import prettier from "eslint-config-prettier";
import react from "eslint-plugin-react";
import reactHooks from "eslint-plugin-react-hooks";
import globals from "globals";

// Patterns start with **/ so the config also works when pre-commit runs it from the repo root.
export default [
  { ignores: ["**/dist/**", "**/node_modules/**"] },
  js.configs.recommended,
  react.configs.flat.recommended,
  react.configs.flat["jsx-runtime"],
  reactHooks.configs.flat.recommended,
  {
    files: ["**/*.{js,jsx}"],
    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "module",
      globals: globals.browser,
    },
    settings: { react: { version: "detect" } },
    rules: { "no-console": "error" },
  },
  {
    files: ["**/*.config.js", "**/vitest.setup.js"],
    languageOptions: { globals: globals.node },
  },
  prettier,
];
