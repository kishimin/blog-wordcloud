import { OpenAPIHono } from "@hono/zod-openapi";
import { swaggerUI } from "@hono/swagger-ui";
import images from "./routes/images/images";

const app = new OpenAPIHono();

app.get("/", (c) => {
  return c.text("Hello Hono!");
});

app.route("/images", images);

app.doc("/docs/json", {
  openapi: "3.0.0",
  info: {
    version: "1.0.0",
    title: "APIドキュメント",
  },
});
app.get("/docs/ui", swaggerUI({ url: "/docs/json" }));

export default app;
