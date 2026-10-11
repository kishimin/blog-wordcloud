import { Hono } from "hono";

const app = new Hono();

app.get("/:entityId", async (c) => {
	try {
		const response = await fetch(process.env.KOTOGUMO_FAST_API);
	} catch (error) {}
});

export default app;
