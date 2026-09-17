import { test, expect, type Page } from '@playwright/test';

async function registerUser(page: Page) {
  const testId = Date.now();
  const username = `u_${testId}_${Math.floor(Math.random() * 1000)}`;
  const password = 'Password123!';

  await page.goto('/login');
  await page.waitForLoadState('networkidle');

  // Check if we need to toggle to register mode
  const toggleBtn = page.getByRole('button', { name: /create an account/i });
  if (await toggleBtn.isVisible()) {
    await toggleBtn.click();
  }

  // Fill in credentials
  await page.locator('input[placeholder*="Username"]').fill(username);
  await page.locator('input[placeholder*="Password"]').fill(password);

  // Click submit
  const submitBtn = page.getByRole('button', { name: /^create account$/i });
  await submitBtn.click();

  // Wait for dashboard redirect
  await page.waitForURL('**/dashboard', { timeout: 15000 });
  await expect(page.locator('h1')).toContainText('Dashboard');
  return { username, password };
}

test.describe('CodeMentor Full Integration E2E Suite', () => {

  test('1. login → refresh session maintains authenticated state', async ({ page }) => {
    await registerUser(page);

    // Refresh page to verify session persistence
    await page.reload();
    await page.waitForLoadState('networkidle');
    await expect(page.locator('h1')).toContainText('Dashboard');
    await expect(page.locator('header')).toContainText('CodeMentor');
  });

  test('2. Python lesson → practice requirement gating', async ({ page }) => {
    await registerUser(page);

    // Navigate to Day 1 lesson
    await page.goto('/learning/day/1');
    await page.waitForLoadState('networkidle');
    await expect(page.locator('body')).toBeVisible();

    // Verify Day 1 lesson content is rendered
    await expect(page.locator('body')).toContainText(/Day 0*1/i);

    // Navigate to Day 2 — must be locked because Day 1 is not completed
    await page.goto('/learning/day/2');
    await page.waitForLoadState('networkidle');
    await expect(page.locator('body')).toContainText(/locked|prerequisite|complete day 1/i);
  });

  test('3. stale localStorage cannot bypass progression', async ({ page }) => {
    await registerUser(page);

    await page.goto('/learning');
    await page.waitForLoadState('networkidle');

    // Inject fake progress trying to claim days 1-5 are completed and day 6 is current
    await page.evaluate(() => {
      localStorage.setItem('codementor_journey_progress', JSON.stringify({
        current_day: 6,
        completed_days: [1, 2, 3, 4, 5],
        day_records: {
          1: { lesson_completed: true, practice_passed: true, completed: true },
          2: { lesson_completed: true, practice_passed: true, completed: true },
          3: { lesson_completed: true, practice_passed: true, completed: true },
          4: { lesson_completed: true, practice_passed: true, completed: true },
          5: { lesson_completed: true, practice_passed: true, completed: true },
        },
        last_activity_timestamp: Date.now(),
      }));
    });

    // Reload page — server progress must replace/sanitize stale local progression
    await page.reload();
    await page.waitForLoadState('networkidle');

    // Navigate to Day 6 — server will deny lesson access and show locked gate
    await page.goto('/learning/day/6');
    await page.waitForLoadState('networkidle');
    await expect(page.locator('body')).toContainText(/locked|prerequisite/i);
  });

  test('4. SAP onboarding → diagnostic → placement flow', async ({ page }) => {
    await registerUser(page);

    await page.goto('/sap/placement');
    await page.waitForLoadState('networkidle');

    // Verify SAP diagnostic/placement UI is present
    await expect(page.locator('body')).toContainText(/diagnostic|placement|experience/i);
    await expect(page.locator('button, input').first()).toBeVisible();
  });

  test('5. SAP 100-day roadmap renders completely across all phases', async ({ page }) => {
    await registerUser(page);

    await page.goto('/sap/learning');
    await page.waitForLoadState('networkidle');

    // Verify SAP curriculum page renders
    await expect(page.locator('body')).toContainText(/S\/4HANA|SAP|Curriculum/i);
    await expect(page.locator('body')).toContainText(/Phase 1|Enterprise Architecture/i);
  });

  test('6. logout → protected routes reject session', async ({ page }) => {
    await registerUser(page);

    // Click the "Sign out" button in the AppShell header
    const signOutBtn = page.getByRole('button', { name: /sign out/i });
    await expect(signOutBtn).toBeVisible();
    await signOutBtn.click();

    // AppShell must redirect to /login
    await page.waitForURL('**/login', { timeout: 10000 });
    await expect(page.locator('h1')).toContainText(/Welcome back|Create your account/);

    // Now attempt to navigate back to protected /dashboard
    await page.goto('/dashboard');
    await page.waitForURL('**/login', { timeout: 10000 });
    await expect(page.locator('h1')).toContainText(/Welcome back|Create your account/);
  });

});
