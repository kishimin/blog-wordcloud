import { createRoute, OpenAPIHono, z } from "@hono/zod-openapi";
import axios from "axios";
import { env } from "hono/adapter";
import {
	EntitiesQueriesSchema,
	EntitiesResponseSchema,
	type Source,
	SourcesResponseSchema,
} from "../../../../schemas/collectors/collectors";
import type { Env } from "../../../../types/env";

const app = new OpenAPIHono();

export const getSources = createRoute({
	method: "get" as const,
	path: "sources",
	summary: "List Sources",
	description: "Get all sources",
	responses: {
		200: {
			description: "success",
			content: {
				"application/json": {
					schema: SourcesResponseSchema,
				},
			},
		},
		500: {
			description: "Internal Server Error",
			content: {
				"application/json": {
					schema: z.object({
						message: z.string().openapi({
							example: "Internal Server Error",
						}),
					}),
				},
			},
		},
	},
});

app.openapi(getSources, async (c) => {
	try {
		const { SLOPE_COLLECTOR_FAST_API_URL } = env<Env>(c);
		const response = await axios.get<{ sources: Source[] }>(
			`${SLOPE_COLLECTOR_FAST_API_URL}/sources`,
		);
		const data = response.data;

		const sources = SourcesResponseSchema.parse(data.sources);

		return c.json(sources, 200);
	} catch {
		return c.json({ message: "外部APIの取得に失敗しました" }, 500);
	}
});

export const getEntities = createRoute({
	method: "get" as const,
	path: "/entities",
	summary: "List Entities",
	description: "Get all Entities of each Source",
	request: {
		query: EntitiesQueriesSchema,
	},
	responses: {
		200: {
			description: "success",
			content: {
				"application/json": {
					schema: EntitiesResponseSchema,
				},
			},
		},
		500: {
			description: "Internal Server Error",
			content: {
				"application/json": {
					schema: z.object({
						message: z.string().openapi({
							example: "Internal Server Error",
						}),
					}),
				},
			},
		},
	},
});

type PythonEntity = {
	id: number;
	source_id: number;
	name: string;
	is_active: boolean;
};

app.openapi(getEntities, async (c) => {
	try {
		const { sourceId } = c.req.query();

		const { SLOPE_COLLECTOR_FAST_API_URL } = env<Env>(c);
		const params = { source_id: sourceId };
		const query = new URLSearchParams(params);
		const response = await axios.get<{ entities: PythonEntity[] }>(
			`${SLOPE_COLLECTOR_FAST_API_URL}/entities?${query}`,
		);
		const data = response.data;

		const sources = EntitiesResponseSchema.parse(
			data.entities.map((entity) => ({
				...entity,
				isActive: entity.is_active,
				sourceId: entity.source_id,
			})),
		);

		return c.json(sources, 200);
	} catch {
		return c.json({ message: "外部APIの取得に失敗しました" }, 500);
	}
});

export default app;
