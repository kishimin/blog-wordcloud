import { expect, test } from "bun:test";
import app from ".";

test("GET /healthは200を返す", async () => {
	const response = await app.request("/health");

	expect(response.status).toBe(200);
});
