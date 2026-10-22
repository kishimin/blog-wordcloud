import { z } from "@hono/zod-openapi";

export const SourceSchema = z
	.object({
		id: z.number().min(1),
		name: z.string(),
	})
	.openapi("Source");

export type Source = z.infer<typeof SourceSchema>;

export const SourcesResponseSchema = z.array(SourceSchema);

export const EntitiesQueriesSchema = z.object({
	sourceId: z
		.string()
		.min(1)
		.regex(/^[1-9][0-9]*$/)
		.openapi({
			param: {
				name: "sourceId",
				in: "query",
			},
		}),
});

export const EntitySchema = z
	.object({
		id: z.number().min(1),
		sourceId: z.number().min(1),
		name: z.string(),
		isActive: z.boolean(),
	})
	.openapi("Entity");

export type Entity = z.infer<typeof EntitySchema>;

export const EntitiesResponseSchema = z.array(EntitySchema);
