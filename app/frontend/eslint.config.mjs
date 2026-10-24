import vitest from "@vitest/eslint-plugin";
import { defineConfig } from "eslint/config";
import jsxA11y from "eslint-plugin-jsx-a11y";
import react from "eslint-plugin-react";
import reactHooks from "eslint-plugin-react-hooks";
import reactRefresh from "eslint-plugin-react-refresh";
import testingLibrary from "eslint-plugin-testing-library";
import globals from "globals";
import { createCommonConfig, testFiles } from "../eslint.config.base.mjs";

export default defineConfig([
	...createCommonConfig(import.meta.dirname, globals.browser),
	{
		files: ["**/*.{ts,tsx}"],
		extends: [
			reactHooks.configs.flat.recommended,
			reactRefresh.configs.vite,
			react.configs.flat.recommended,
			jsxA11y.flatConfigs.recommended,
		],
		settings: { react: { version: "detect" } },
		rules: {
			"react/jsx-key": ["error", { checkFragmentShorthand: true }],
			"react/react-in-jsx-scope": "off",
			"react/jsx-uses-react": "off",
		},
	},
	{
		files: testFiles,
		extends: [testingLibrary.configs["flat/react"], vitest.configs.recommended],
		rules: {
			"@typescript-eslint/no-unsafe-call": "off",
			"@typescript-eslint/no-unsafe-member-access": "off",
			"vitest/max-nested-describe": ["error", { max: 3 }],
			"vitest/no-focused-tests": "error",
			"vitest/no-disabled-tests": "warn",
		},
		settings: { vitest: { typecheck: true } },
		languageOptions: { globals: vitest.environments.env.globals },
	},
	{
		files: testFiles,
		ignores: ["src/**"],
		// These tests are outside the TypeScript project used by typed linting.
		settings: { vitest: { typecheck: false } },
	},
	{
		files: ["*.{js,mjs,ts}", ".storybook/**/*.{ts,tsx}"],
		languageOptions: { globals: globals.node },
	},
]);
