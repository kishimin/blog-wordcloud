import react from "@vitejs/plugin-react";
import { defineConfig } from "vitest/config";

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    setupFiles: ["./src/tests/setup.ts"],
    coverage: {
      provider: "v8",
      include: ["src/**/*.{ts,tsx}"],
      reporter: ["text", "html", "lcov", "json-summary"],
      reportsDirectory: "./coverage",
      exclude: [
        "src/tests/**",
        "src/vite-env.d.ts",
        // Mounts <App /> and guards against a missing #root element. That
        // guard is unreachable unless index.html's markup changes, so it is
        // a defensive check with no meaningful branch to exercise, not
        // behavior worth a test. Delete this line if that changes.
        "src/main.tsx",
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
