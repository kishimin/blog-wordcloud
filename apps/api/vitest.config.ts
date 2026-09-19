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
      thresholds: {
        lines: 80,
        statements: 80,
        functions: 80,
        branches: 80,
      },
    },
  },
});
