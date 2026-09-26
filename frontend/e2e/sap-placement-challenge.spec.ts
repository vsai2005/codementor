import { test, expect, type Page } from '@playwright/test';

// Placement lifecycle + waived-day challenge through the real UI and backend:
// a learner placed at Day 9 (Days 1-8 waived) earns Day 6's concepts via its challenge,
// the day stays waived, and placement becomes locked because learning evidence now exists.
const NOT_SURE_ALL_CORRECT = {
  ns_fund_01: 'b', ns_org_02: 'b', ns_data_03: 'a', ns_p2p_04: 'b', ns_hana_05: 'a', ns_fiori_06: 'b',
};

async function registerUser(page: Page) {
  const id = `${Date.now()}_${Math.floor(Math.random() * 100000)}`;
  await page.goto('/login');
  await page.waitForLoadState('networkidle');
  const toggle = page.getByRole('button', { name: /create an account/i });
  if (await toggle.isVisible()) await toggle.click();
  await page.locator('input[placeholder*="Username"]').fill(`plc_${id}`);
  await page.locator('input[placeholder*="Password"]').fill(`Pw!${id}x`);
  await page.getByRole('button', { name: /^create account$/i }).click();
  await page.waitForURL('**/dashboard', { timeout: 25000 });
}

async function api(page: Page, method: string, path: string, body?: unknown) {
  return page.evaluate(
    async ({ method, path, body }) => {
      const res = await fetch(path, {
        method,
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: body === undefined ? undefined : JSON.stringify(body),
      });
      return { status: res.status, json: await res.json().catch(() => null) };
    },
    { method, path, body },
  );
}

test('waived learner earns a skipped day via its challenge; placement then locks', async ({ page }) => {
  test.setTimeout(90000);
  await registerUser(page);

  const placed = await api(page, 'POST', '/api/sap/placement/submit', {
    experience_level: 'not_sure', answers: NOT_SURE_ALL_CORRECT,
  });
  expect(placed.status).toBe(200);
  expect(placed.json.recommended_start_day).toBe(9);
  expect(placed.json.placement_locked).toBe(false);

  // Waived lesson stays closed; roadmap offers the challenge instead.
  expect((await api(page, 'GET', '/api/sap/learning/lessons/6')).status).toBe(403);
  await page.goto('/sap/learning');
  await expect(page.getByRole('link', { name: /TAKE CHALLENGE/i }).first()).toBeVisible();

  // Take Day 6's challenge: first wrong, then right.
  await page.goto('/sap/learning/day/6/challenge');
  await expect(page.locator('h1')).toContainText(/Day 6/);
  await page.locator('input[name="d6_q1"][value="b"]').check();
  await page.locator('input[name="d6_q2"][value="b"]').check();
  await page.getByRole('button', { name: /Submit Challenge/i }).click();
  await expect(page.getByText(/Challenge not passed/i)).toBeVisible();

  await page.getByRole('button', { name: /Try again/i }).click();
  await page.locator('input[name="d6_q1"][value="a"]').check();
  await page.locator('input[name="d6_q2"][value="a"]').check();
  await page.getByRole('button', { name: /Submit Challenge/i }).click();
  await expect(page.getByText(/Challenge passed/i)).toBeVisible();

  // Day 6 is still waived, current day unchanged, lesson still closed.
  const progress = await api(page, 'GET', '/api/sap/learning/progress');
  expect(progress.json.day_states['6'].waived).toBe(true);
  expect(progress.json.current_day).toBe(9);
  expect(progress.json.completed_days).toEqual([]);
  expect((await api(page, 'GET', '/api/sap/learning/lessons/6')).status).toBe(403);

  // Placement is now locked: API refuses, UI explains and hides retake.
  const retake = await api(page, 'POST', '/api/sap/placement/submit', { experience_level: 'fresher', answers: {} });
  expect(retake.status).toBe(409);
  await page.goto('/sap/placement');
  await expect(page.getByText(/Placement locked/i)).toBeVisible();
  await expect(page.getByText(/OPTION 1/)).toHaveCount(0);
});
