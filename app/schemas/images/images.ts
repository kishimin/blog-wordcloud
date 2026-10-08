import * as z from "zod";

export const imageSchema = z.object({
	entityId: z.number("数値です").int("整数です").min(1, "1以上です"),
});
