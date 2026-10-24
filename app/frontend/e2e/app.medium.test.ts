import { expect, test } from "@playwright/test";

test("クリックするとカウンターが増える", async ({ page }) => {
	await page.goto("/");
	const counter = page.getByRole("button", { name: "Count is 0", exact: true });
	await expect(counter).toBeVisible();
	await counter.click();
	await expect(
		page.getByRole("button", { name: "Count is 1", exact: true }),
	).toBeVisible();
});
