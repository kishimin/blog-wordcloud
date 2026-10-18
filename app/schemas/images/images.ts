import { z } from "@hono/zod-openapi";

export const ParamsSchema = z.object({
	entityId: z
		.string()
		.min(1, "必須です")
		.regex(/\d/, "数値です")
		.openapi({
			param: {
				name: "entityId",
				in: "path",
			},
		}),
});

export const ResponseSchema = z
	.object({
		image: z
			.file()
			.min(1)
			.mime("image/png")
			.openapi({ type: "string", format: "binary" }),
	})
	.openapi("Image");

export type GetImageResponse = z.infer<typeof ResponseSchema>;
