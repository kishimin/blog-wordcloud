import vitest from "@vitest/eslint-plugin";
import { defineConfig } from "eslint/config";
import globals from "globals";
import { createCommonConfig, testFiles } from "../eslint.config.base.mjs";

export default defineConfig([
	...createCommonConfig(import.meta.dirname, {
		...globals.node,
		Bun: "readonly",
	}),
	{
		files: testFiles,
		extends: [vitest.configs.recommended],
		rules: {
			"@typescript-eslint/no-unsafe-call": "off",
			"@typescript-eslint/no-unsafe-member-access": "off",
			"vitest/max-nested-describe": ["error", { max: 3 }],
			"vitest/no-focused-tests": "error",
			"vitest/no-disabled-tests": "warn",
		},
		settings: { vitest: { typecheck: true, vitestImports: ["bun:test"] } },
	},
	{
		files: testFiles,
		ignores: ["src/**"],
		// These tests are outside the TypeScript project used by typed linting.
		settings: { vitest: { typecheck: false } },
	},
	{
		files: ["*.mjs"],
		languageOptions: { globals: globals.node },
	},
]);
