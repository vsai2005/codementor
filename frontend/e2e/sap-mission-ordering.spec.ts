import { test, expect, type Page } from '@playwright/test';

// Completes nova-org-structure-design end-to-end through the real UI and backend,
// including its order_process step. The browser never receives the correct order: the
// learner (this test) knows the hierarchy and arranges the server's randomized items.
const MISSION = 'nova-org-structure-design';
const HIERARCHY = ['Client (100)', 'Company Code (NM01)', 'Plant (PL01)', 'Storage Location (RM01)'];

async function registerUser(page: Page) {
  const id = `${Date.now()}_${Math.floor(Math.random() * 100000)}`;
  await page.goto('/login');
  await page.waitForLoadState('networkidle');
  const toggle = page.getByRole('button', { name: /create an account/i });
  if (await toggle.isVisible()) await toggle.click();
  await page.locator('input[placeholder*="Username"]').fill(`ord_${id}`);
  await page.locator('input[placeholder*="Password"]').fill(`Pw!${id}x`);
  await page.getByRole('button', { name: /^create account$/i }).click();
  await page.waitForURL('**/dashboard', { timeout: 25000 });
}

async function currentOrder(page: Page): Promise<string[]> {
  const items = page.locator('ol[aria-labelledby="order-legend"] > li');
  const n = await items.count();
  const out: string[] = [];
  for (let i = 0; i < n; i++) {
    const label = await items.nth(i).locator('span').first().innerText();
    out.push(label.replace(/^\s*\d+\.\s*/, '').trim());
  }
  return out;
}

async function arrange(page: Page, target: string[]) {
  // Selection-sort using the per-item "Move up" buttons.
  for (const [pos, item] of target.entries()) {
    let order = await currentOrder(page);
    let idx = order.indexOf(item);
    while (idx > pos) {
      await page.getByRole('button', { name: `Move ${item} up` }).click();
      idx -= 1;
    }
    order = await currentOrder(page);
    expect(order[pos]).toBe(item);
  }
}

test('SAP mission with an ordering step completes end-to-end from the browser', async ({ page }) => {
  test.setTimeout(90000);
  await registerUser(page);

  const attempts: Array<Record<string, unknown>> = [];
  page.on('request', (req) => {
    if (req.url().includes(`/api/sap/missions/${MISSION}/attempt`) && req.method() === 'POST') {
      attempts.push(JSON.parse(req.postData() || '{}'));
    }
  });
  let detailBody = '';
  page.on('response', async (res) => {
    if (res.url().match(new RegExp(`/api/sap/missions/${MISSION}(\\?|$)`)) && res.request().method() === 'GET') {
      detailBody = await res.text().catch(() => detailBody);
    }
  });

  await page.goto(`/sap/missions/${MISSION}`);
  await expect(page.locator('h1')).toContainText(/Organizational Hierarchy/i);

  // The mission detail payload carries no answer key.
  expect(detailBody).not.toMatch(/correct_order|is_correct|explanation|expected_state_patch/);

  const execute = page.getByRole('button', { name: /Execute & Validate Step/i });

  // Step 1 and 2: option steps
  await page.getByLabel(/Company Code NM01 \(EUR\)/).check();
  await execute.click();
  await expect(page.getByText('✓ Step Verified Successfully')).toBeVisible();
  await page.getByRole('button', { name: /Proceed to Step 2/i }).click();

  await page.getByLabel(/Assign Plant PL01 to Company Code NM01/).check();
  await execute.click();
  await expect(page.getByText('✓ Step Verified Successfully')).toBeVisible();
  await page.getByRole('button', { name: /Proceed to Step 3/i }).click();

  // Step 3: ordering. A wrong arrangement is rejected by the server...
  await expect(page.locator('ol[aria-labelledby="order-legend"] > li')).toHaveCount(4);
  await arrange(page, [...HIERARCHY].reverse());
  await execute.click();
  await expect(page.getByText('✗ Step Verification Failed')).toBeVisible();

  // ...and the correct arrangement completes the mission.
  await arrange(page, HIERARCHY);
  await execute.click();
  await expect(page.getByRole('heading', { name: /Mission Accomplished/i })).toBeVisible();

  // Choice steps sent selected_option_id; the ordering step sent only ordered_items.
  const payloads = attempts.map((a) => a.payload as Record<string, unknown>);
  expect(payloads.slice(0, 2).every((p) => typeof p.selected_option_id === 'string' && !('ordered_items' in p))).toBe(true);
  expect(payloads.slice(2).every((p) => Array.isArray(p.ordered_items) && !('selected_option_id' in p))).toBe(true);
  expect(payloads.at(-1)?.ordered_items).toEqual(HIERARCHY);

  // Server state agrees: the mission is completed at 100.
  const missions = await page.evaluate(async () => (await fetch('/api/sap/missions', { credentials: 'include' })).json());
  const m = missions.find((x: { slug: string }) => x.slug === 'nova-org-structure-design');
  expect(m.passed).toBe(true);
  expect(m.score).toBe(100);
});
