import { expect, test } from "@playwright/test";

test("SourceとEntityを選ぶと、そのEntityのよく使う言葉をまとめた画像が表示される", async ({
  page,
}) => {
  await test.step("navigate", () => {
    page.goto("/");
  });

  await test.step("Select Source", async () => {
    await page
      .getByRole("listbox", { name: import.meta.env.SOURCE_JA_LABEL })
      .click();

    await page
      .getByRole("option", { name: import.meta.env.SOURCE_OPTION_NAME })
      .click();
  });
  await test.step("Select Entity", async () => {
    await page
      .getByRole("listbox", { name: import.meta.env.ENTITY_JA_LABEL })
      .click();
    await page
      .getByRole("option", { name: import.meta.env.ENTITY_OPTION_NAME })
      .click();
  });

  await page.getByRole("button", { name: "よく使う言葉を見てみる" }).click();

  await expect(page.getByRole("img")).toBeVisible();
});
