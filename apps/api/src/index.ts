import { serve } from "@hono/node-server";
import { app } from "./app";
import { parsePort } from "./port";

const port = parsePort(process.env.PORT);

serve({ fetch: app.fetch, port }, (info) => {
  console.log(`Kotogumo API listening on http://localhost:${info.port}`);
});
