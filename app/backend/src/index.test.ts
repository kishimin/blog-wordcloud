import { describe, expect, test } from "bun:test";
import app from ".";

describe("エントリーポイントのテスト", () => {
	test("/にアクセスすると、200である", async () => {
		const response = await app.request("/", { method: "GET" });
		expect(response.status).toBe(200);
	});
});
