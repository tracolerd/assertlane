import { test, expect } from '@playwright/test';
// AssertLane-এর Test Case ID ট্যাগের মাধ্যমে যুক্ত করা হয়েছে
test('AssertLane Demo App Loads @TID-072af62d-6a30-47f6-84e2-a88fe0ddf68f', async ({ page }) => {
  await page.goto('/demo');
  await expect(page).toHaveTitle(/AssertLane Demo/);
  await expect(page.locator('h1')).toContainText('Welcome to AssertLane');
});
