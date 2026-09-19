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
        // Scaffolding with no decision of its own: it only starts the HTTP
        // server and wires app.fetch to it. A test would restate that
        // wiring instead of proving behavior, so it stays out of the
        // denominator until it gains logic worth covering. Delete this
        // line then.
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
