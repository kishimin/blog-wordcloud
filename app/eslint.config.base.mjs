import js from "@eslint/js";
import { defineConfig, globalIgnores } from "eslint/config";
import prettier from "eslint-config-prettier";
import importPlugin from "eslint-plugin-import";
import { jsdoc } from "eslint-plugin-jsdoc";
import unusedImports from "eslint-plugin-unused-imports";
import tseslint from "typescript-eslint";

export const testFiles = [
	"**/*.test.{ts,tsx}",
	"**/*.spec.{ts,tsx}",
	"**/__tests__/**/*.{ts,tsx}",
	"**/tests/**/*.{ts,tsx}",
];

export const createCommonConfig = (tsconfigRootDir, runtimeGlobals) =>
	defineConfig([
		globalIgnores(["**/dist/**", "**/coverage/**", "**/storybook-static/**"]),
		js.configs.recommended,
		{
			files: ["**/*.{ts,tsx}"],
			extends: [
				tseslint.configs.recommended,
				importPlugin.flatConfigs.recommended,
				importPlugin.flatConfigs.typescript,
			],
			settings: {
				"import/resolver": {
					typescript: {
						project: `${tsconfigRootDir}/tsconfig.json`,
						bun: true,
					},
					node: true,
				},
			},
			languageOptions: {
				ecmaVersion: 2020,
				globals: runtimeGlobals,
				parserOptions: { tsconfigRootDir },
			},
			rules: {
				"no-console": "warn",
				camelcase: ["warn", { properties: "never" }],
				"@typescript-eslint/no-explicit-any": "warn",
				"@typescript-eslint/no-unnecessary-type-assertion": "off",
				"import/order": [
					"error",
					{ alphabetize: { order: "asc", caseInsensitive: true } },
				],
			},
		},
		{
			files: ["src/**/*.{ts,tsx}"],
			extends: [tseslint.configs.recommendedTypeChecked],
			languageOptions: {
				parserOptions: { projectService: true, tsconfigRootDir },
			},
			rules: {
				"@typescript-eslint/switch-exhaustiveness-check": "warn",
				"@typescript-eslint/no-explicit-any": "warn",
				"@typescript-eslint/no-unnecessary-type-assertion": "off",
			},
		},
		{
			plugins: { "unused-imports": unusedImports },
			rules: {
				"no-unused-vars": "off",
				"@typescript-eslint/no-unused-vars": "off",
				"unused-imports/no-unused-imports": "error",
				"unused-imports/no-unused-vars": [
					"warn",
					{
						vars: "all",
						varsIgnorePattern: "^_",
						args: "after-used",
						argsIgnorePattern: "^_",
					},
				],
			},
		},
		jsdoc({
			config: "flat/recommended",
			rules: {
				"jsdoc/require-param": "off",
				"jsdoc/require-returns": "off",
				"jsdoc/require-description": "off",
				"jsdoc/check-values": ["error", { allowedLicenses: ["MIT", "ISC"] }],
				"jsdoc/require-jsdoc": [
					"error",
					{
						publicOnly: true,
						require: {
							FunctionDeclaration: true,
							MethodDefinition: true,
							ClassDeclaration: true,
						},
					},
				],
			},
			settings: {
				structuredTags: {
					see: { name: "namepath-referencing", required: ["name"] },
				},
			},
		}),
		prettier,
	]);
