import { z } from "@hono/zod-openapi";

export const ParamsSchema = z.object({
	entityId: z
		.number("数値です")
		.int("整数です")
		.min(1, "1以上です")
		.openapi({
			param: {
				name: "entityId",
				in: "path",
			},
			example: "8",
		}),
});

export const ResponseSchema = z
	.object({
		image: z.file().min(1).mime("image/png"),
	})
	.openapi("Image");

export type GetImageResponse = z.infer<typeof ResponseSchema>;
