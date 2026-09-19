import { cleanup } from "@testing-library/react";
import { afterEach } from "vitest";
import "@testing-library/jest-dom/vitest";

// Without an explicit cleanup, DOM trees rendered by one test stay mounted
// for the next test in the same file (this config has no `globals: true`,
// so Testing Library's automatic afterEach cleanup has no afterEach to hook
// into), which breaks role-based queries like getByRole once a file has
// more than one test.
afterEach(() => {
  cleanup();
});
