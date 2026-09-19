import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    environment: "node",
    coverage: {
      provider: "v8",
      include: ["src/**/*.ts"],
      reporter: ["text", "html", "lcov", "json-summary"],
      reportsDirectory: "./coverage",
      exclude: [
        // Pure wiring: it delegates every decision (port validation) to the
        // tested parsePort helper and only calls serve() with the result. A
        // test here would just re-assert that delegation, not prove new
        // behavior, so it stays out of the denominator until it makes a
        // decision of its own. Delete this line then.
        "src/index.ts",
      ],
      // 80% is the default so a bare local `vitest run --coverage` still
      // enforces it. CI opts OUT by setting COVERAGE_THRESHOLD=0 for push
      // (Small only) and nightly, whose narrower or differently scoped
      // ADR-0043 test set must not fail the build over code a different
      // test size is meant to cover; the pull_request gate leaves it unset
      // and gets the enforced default. Kept in sync with the identical
      // block in apps/frontend/vite.config.ts.
      thresholds:
        process.env.COVERAGE_THRESHOLD === "0"
          ? undefined
          : {
              lines: 80,
              statements: 80,
              functions: 80,
              branches: 80,
            },
    },
  },
});
