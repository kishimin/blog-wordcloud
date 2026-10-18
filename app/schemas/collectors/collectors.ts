import { z } from "@hono/zod-openapi";

export const SourcesResponseSchema = z.array(
	z
		.object({
			id: z.number().min(1),
			name: z.string(),
		})
		.openapi("Source"),
);

export const EntitiesQueriesSchema = z.object({
	sourceId: z
		.string()
		.min(1)
		.regex(/\d/)
		.openapi({
			param: {
				name: "sourceId",
				in: "query",
			},
		}),
});

export const EntitiesResponseSchema = z.array(
	z
		.object({
			id: z.number().min(1),
			source_id: z.number().min(1),
			name: z.string(),
			is_active: z.boolean(),
		})
		.transform(({ source_id, is_active, id, name }) => {
			return { id, sourceId: source_id, name, isActive: is_active };
		})
		.openapi("Entity"),
);
