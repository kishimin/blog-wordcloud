import { OpenAPIHono } from "@hono/zod-openapi";
import { z, createRoute } from "@hono/zod-openapi";
import {
  ParamsSchema,
  ResponseSchema,
} from "../../../../schemas/images/images";
import { env } from "hono/adapter";
import { Env } from "../../../../types/env";

const app = new OpenAPIHono();

export const getWordCloudImage = createRoute({
  method: "get" as const,
  path: "/{entityId}",
  summary: "get wordcloud image",
  description: "entityIdのワードクラウドを取得する",
  request: {
    params: ParamsSchema,
  },
  responses: {
    200: {
      description: "success",
      content: {
        "image/png": {
          schema: ResponseSchema,
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

app.openapi(getWordCloudImage, async (c) => {
  try {
    const { entityId } = c.req.param();

    const { KOTOGUMO_FAST_API_URL } = env<Env>(c);
    const response = await fetch(`${KOTOGUMO_FAST_API_URL}/images/${entityId}`);

    const pngBuffer = await response.arrayBuffer();

    return c.body(pngBuffer, 200, {
      "Content-Type": "image/png",
    });
  } catch (error) {
    return c.json({ error: "外部APIの取得に失敗しました" }, 500);
  }
});

export default app;
