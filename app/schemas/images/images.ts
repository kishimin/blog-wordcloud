import * as z from "zod";

export const imageSchema = z.object({
	entityId: z.number(),
});
