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
      // 80% is the default so a bare local `vitest run --coverage` still
      // enforces it. CI opts OUT by setting COVERAGE_THRESHOLD=0 for push
      // (Small only) and nightly, whose narrower or differently scoped
      // ADR-0043 test set must not fail the build over code a different
      // test size is meant to cover; the pull_request gate leaves it unset
      // and gets the enforced default. Kept in sync with the identical
      // block in apps/api/vitest.config.ts.
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
