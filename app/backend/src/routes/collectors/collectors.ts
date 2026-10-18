import { createRoute, OpenAPIHono, z } from "@hono/zod-openapi";
import {
  EntitiesQueriesSchema,
  EntitiesResponseSchema,
  SourcesResponseSchema,
} from "../../../../schemas/collectors/collectors";
import { env } from "hono/adapter";
import { Env } from "../../../../types/env";

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
    const response = await fetch(`${SLOPE_COLLECTOR_FAST_API_URL}/sources`);
    const data = await response.json();

    const sources = SourcesResponseSchema.parse(data.sources);

    return c.json(sources, 200);
  } catch (error) {
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

app.openapi(getEntities, async (c) => {
  try {
    const { sourceId } = c.req.query();

    const { SLOPE_COLLECTOR_FAST_API_URL } = env<Env>(c);
    const params = { source_id: sourceId };
    const query = new URLSearchParams(params);
    const response = await fetch(
      `${SLOPE_COLLECTOR_FAST_API_URL}/entities?${query}`,
    );

    const data = await response.json();

    const sources = EntitiesResponseSchema.parse(data.entities);

    return c.json(sources, 200);
  } catch (error) {
    return c.json({ message: "外部APIの取得に失敗しました" }, 500);
  }
});

export default app;
