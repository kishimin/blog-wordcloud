import { describe, expect, it } from "vitest";
import { app } from "./app";

describe("GET /health", () => {
  it("responds with 200 and an ok status", async () => {
    const res = await app.request("/health");

    expect(res.status).toBe(200);
    await expect(res.json()).resolves.toEqual({ status: "ok" });
  });
});
