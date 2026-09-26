import { test, expect, type Page } from '@playwright/test';

// Auth flows against the real backend with production rate-limit and body-size defaults.
const id = () => `${Date.now()}_${Math.floor(Math.random() * 100000)}`;

async function fetchJson(page: Page, path: string, body: unknown) {
  return page.evaluate(
    async ({ path, body }) => {
      const res = await fetch(path, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });
      return { status: res.status, retryAfter: res.headers.get('retry-after'), json: await res.json().catch(() => null) };
    },
    { path, body },
  );
}

async function openForm(page: Page, mode: 'login' | 'register') {
  await page.goto('/login');
  await page.waitForLoadState('networkidle');
  if (mode === 'register') {
    const toggle = page.getByRole('button', { name: /create an account/i });
    if (await toggle.isVisible()) await toggle.click();
  }
}

test('register, sign out, wrong password, then sign in', async ({ page }) => {
  const username = `auth_${id()}`;
  const password = `Pw!${id()}x`;

  await openForm(page, 'register');
  await page.locator('input[placeholder*="Username"]').fill(username);
  await page.locator('input[placeholder*="Password"]').fill(password);
  await page.getByRole('button', { name: /^create account$/i }).click();
  await page.waitForURL('**/dashboard', { timeout: 25000 });

  expect((await fetchJson(page, '/api/auth/logout', {})).status).toBe(200);

  await openForm(page, 'login');
  await page.locator('input[placeholder="Username or email"]').fill(username);
  await page.locator('input[placeholder="Password"]').fill('definitely-wrong');
  await page.getByRole('button', { name: /^sign in$/i }).click();
  await expect(page.locator('p[role="alert"]')).toContainText(/Incorrect username\/email or password/i);

  await page.locator('input[placeholder="Password"]').fill(password);
  await page.getByRole('button', { name: /^sign in$/i }).click();
  await page.waitForURL('**/dashboard', { timeout: 25000 });
});

test('repeated attempts on one account are throttled with 429 and a clear message', async ({ page }) => {
  await page.goto('/login');
  const target = `nobody_${id()}`;
  const codes: number[] = [];
  for (let i = 0; i < 10; i++) {
    codes.push((await fetchJson(page, '/api/auth/login', { identifier: target, password: 'x' })).status);
  }
  expect(codes).toEqual(Array(10).fill(401));
  const blocked = await fetchJson(page, '/api/auth/login', { identifier: target, password: 'x' });
  expect(blocked.status).toBe(429);
  expect(Number(blocked.retryAfter)).toBeGreaterThan(0);

  await openForm(page, 'login');
  await page.locator('input[placeholder="Username or email"]').fill(target);
  await page.locator('input[placeholder="Password"]').fill('x');
  await page.getByRole('button', { name: /^sign in$/i }).click();
  await expect(page.locator('p[role="alert"]')).toContainText(/Too many attempts/i);
});

test('oversized login body is rejected with 413 and no session', async ({ page }) => {
  await page.goto('/login');
  const res = await fetchJson(page, '/api/auth/login', { identifier: 'x'.repeat(200_000), password: 'p' });
  expect(res.status).toBe(413);
  expect(res.json.detail).toMatch(/too large/i);
  const me = await page.evaluate(async () => (await fetch('/api/auth/me', { credentials: 'include' })).status);
  expect(me).toBe(401);
});
