import { expect, test } from '@playwright/test';

test('Monaco editor sends typed code to the real run endpoint and shows results', async ({ page }) => {
  test.setTimeout(60000);
  const unique = `${Date.now()}_${Math.floor(Math.random() * 100000)}`;
  await page.goto('/login');
  await page.getByRole('button', { name: /create an account/i }).click();
  await page.locator('input[placeholder*="Username"]').fill(`editor_${unique}`);
  await page.locator('input[placeholder*="Password"]').fill(`Pw!${unique}x`);
  await page.getByRole('button', { name: /^create account$/i }).click();
  await page.waitForURL('**/dashboard', { timeout: 25000 });

  const list = await page.request.get('/api/problems?page_size=1');
  expect(list.ok()).toBeTruthy();
  const firstProblem = (await list.json()).items[0];
  expect(firstProblem?.id).toBeTruthy();
  const detail = await page.request.get(`/api/problems/${firstProblem.id}`);
  expect(detail.ok()).toBeTruthy();
  const { entry_point: entryPoint } = await detail.json();

  await page.goto(`/practice/${firstProblem.id}`);
  const editor = page.locator('.monaco-editor');
  await expect(editor).toBeVisible({ timeout: 20000 });
  await editor.click();
  await page.keyboard.press('ControlOrMeta+A');
  const code = `def ${entryPoint}(*args):\n    return None\n# batch7-editor-regression`;
  await page.keyboard.insertText(code);

  const responsePromise = page.waitForResponse((response) =>
    response.url().endsWith('/api/submissions/run') && response.request().method() === 'POST',
  );
  await page.getByRole('button', { name: /^Run$/ }).click();
  const response = await responsePromise;
  expect(response.request().postDataJSON().code).toContain('# batch7-editor-regression');
  expect(response.status()).toBe(200);
  await expect(page.getByText('Test results')).toBeVisible();
  await expect(page.getByText(/Case 1/)).toBeVisible();
});
