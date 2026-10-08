import { describe, expect, test } from "bun:test";
import { imageSchema } from "./images";

describe("Image Schemas", () => {
	describe("entityId", () => {
		test("1の時エラーとならない", () => {
			const result = imageSchema.safeParse({ entityId: 1 });

			expect(result.success).toBe(true);
		});

		test("0以下の時エラーとなる", () => {
			const result = imageSchema.safeParse({ entityId: 0 });

			expect(result.success).toBe(false);
			expect(result.error?.issues[0].message).toBe("1以上です");
		});

		test("数値でない時エラーとなる", () => {
			const result = imageSchema.safeParse({ entityId: "1" });

			expect(result.success).toBe(false);
			expect(result.error?.issues[0].message).toBe("数値です");
		});

		test("整数でない時エラーとなる", () => {
			const result = imageSchema.safeParse({ entityId: 1.1 });

			expect(result.success).toBe(false);
			expect(result.error?.issues[0].message).toBe("整数です");
		});
	});
});
