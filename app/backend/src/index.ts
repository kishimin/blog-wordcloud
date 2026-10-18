import { createRoute, OpenAPIHono, z } from "@hono/zod-openapi";
import { swaggerUI } from "@hono/swagger-ui";
import images from "./routes/images/images";
import collectors from "./routes/collectors/collectors";

const app = new OpenAPIHono();

const getHealth = createRoute({
  method: "get" as const,
  path: "/health",
  summary: "Get Health",
  description: "Report that the application process can serve requests.",
  responses: {
    200: {
      description: "success",
      content: {
        "application/json": { schema: z.object({ status: z.string() }) },
      },
    },
  },
});

app.openapi(getHealth, (c) => {
  return c.json({ status: "ok" }, 200);
});

app.route("/images", images);
app.route("/collectors", collectors);

app.doc("/docs/json", {
  openapi: "3.0.0",
  info: {
    version: "1.0.0",
    title: "APIドキュメント",
  },
});
app.get("/docs/ui", swaggerUI({ url: "/docs/json" }));

export default app;
