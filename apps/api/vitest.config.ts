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
      // Enforced only when CI sets COVERAGE_THRESHOLD (the pull_request
      // gate). Coverage is collected on every event, but a hardcoded 80%
      // here would also apply to push (Small only) and nightly, which run a
      // narrower or differently scoped ADR-0043 test set than "overall".
      thresholds: process.env.COVERAGE_THRESHOLD
        ? {
            lines: Number(process.env.COVERAGE_THRESHOLD),
            statements: Number(process.env.COVERAGE_THRESHOLD),
            functions: Number(process.env.COVERAGE_THRESHOLD),
            branches: Number(process.env.COVERAGE_THRESHOLD),
          }
        : undefined,
    },
  },
});
