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
        // Scaffolding with no decision of its own: main.tsx only mounts
        // <App /> into the DOM. A test over it would restate that wiring
        // instead of proving behavior, so it stays out of the denominator
        // until it gains logic worth covering. Delete this line then.
        "src/main.tsx",
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
