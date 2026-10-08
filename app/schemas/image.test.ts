import { describe, expect, test } from "bun:test";
import { imageSchema } from "./image";

describe("Image Schemas", () => {
	test("entityIdが1の時エラーとならない", () => {
		const result = imageSchema.safeParse({ entityId: 1 });

		expect(result.success).toBe(true);
	});
});
