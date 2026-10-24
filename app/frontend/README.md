# React + TypeScript + Vite

## Browser tests

Run these commands from `app/frontend` after installing the workspace dependencies:

```sh
bunx --no-install playwright install chromium
bun run test:e2e
```

Use `bun run test:e2e:ui` for the interactive runner. Playwright starts and stops
Vite on `127.0.0.1:4173`; the port must be available. HTML reports are written to
`playwright-report/`, and failure traces and screenshots to `test-results/`.
These generated directories are ignored by Git.

Tests live in `e2e/` and use `.small.test.ts`, `.medium.test.ts`, or `.large.test.ts`
according to their dependencies. The initial counter test is Medium because it
uses a local Vite server and browser without external services. It checks the
current scaffold; word-cloud display and download acceptance tests are pending
implementation of those features.

Storybook uses its separate Vitest runner (`bun run test:storybook`).

This template provides a minimal setup to get React working in Vite with HMR and some Oxlint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the Oxlint configuration

If you are developing a production application, we recommend enabling type-aware lint rules by installing `oxlint-tsgolint` and editing `.oxlintrc.json`:

```json
{
  "$schema": "./node_modules/oxlint/configuration_schema.json",
  "plugins": ["react", "typescript", "oxc"],
  "options": {
    "typeAware": true
  },
  "rules": {
    "react/rules-of-hooks": "error",
    "react/only-export-components": ["warn", { "allowConstantExport": true }]
  }
}
```

See the [Oxlint rules documentation](https://oxc.rs/docs/guide/usage/linter/rules) for the full list of rules and categories.
