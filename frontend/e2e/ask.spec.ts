import { expect, test } from "@playwright/test";

test("ask a question, see a cited answer, open the source passage", async ({ page }) => {
  await page.goto("/");

  await page.getByLabel("Your question").fill("What is the fuel levy?");
  await page.getByRole("button", { name: "Ask" }).click();

  await expect(page.getByTestId("answer")).toContainText("14.5%");
  const citation = page.getByTestId("citation").first();
  await expect(citation).toContainText("Rate card 2026");

  await citation.click();

  const passage = page.getByTestId("passage");
  await expect(passage).toContainText("Rate card 2026");
  await expect(passage.locator("mark")).toContainText("A fuel levy of 14.5%");
});
