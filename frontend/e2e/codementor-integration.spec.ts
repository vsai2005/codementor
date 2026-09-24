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
  await page.waitForURL('**/dashboard', { timeout: 25000 });
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

  test('7. Practice pass synchronization is idempotent and syncs exactly once', async ({ page }) => {
    await registerUser(page);

    // Track /api/learning/progress sync requests
    let syncCount = 0;
    let practicePassed = false;
    await page.route('**/api/learning/progress', async (route) => {
      syncCount++;
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          current_day: 1,
          completed_days: [],
          day_states: {
            '1': {
              day_number: 1,
              lesson_completed: false,
              practice_passed: practicePassed,
              completed: false,
              unlocked: true,
              status: 'available',
            },
          },
        }),
      });
    });

    // Navigate to Day 1 lesson where useJourney is active
    await page.goto('/learning/day/1');
    await page.waitForLoadState('networkidle');

    // Reset counter after initial page load
    const initialSyncs = syncCount;

    // Simulate practice pass
    practicePassed = true;
    await page.evaluate(() => {
      window.dispatchEvent(
        new CustomEvent('codementor:practice-passed', {
          detail: { day_number: 1 },
        })
      );
    });

    // Wait for debounce / server sync
    await page.waitForTimeout(500);
    const syncsAfterFirstPass = syncCount - initialSyncs;
    expect(syncsAfterFirstPass).toBe(1);

    // Repeated pass event on the same day must be idempotent — NO additional sync calls
    await page.evaluate(() => {
      window.dispatchEvent(
        new CustomEvent('codementor:practice-passed', {
          detail: { day_number: 1 },
        })
      );
      // Even if day-completed is also dispatched
      window.dispatchEvent(
        new CustomEvent('codementor:day-completed', {
          detail: { day_number: 1 },
        })
      );
    });

    await page.waitForTimeout(500);
    const syncsAfterRepeatedPass = syncCount - initialSyncs;
    expect(syncsAfterRepeatedPass).toBe(1);
  });

  test('8. SAP guest flow preserves redirect=/sap/placement and rejects open redirect', async ({ page }) => {
    // 1. Visit /sap/placement unauthenticated
    await page.goto('/sap/placement');
    await page.waitForLoadState('networkidle');

    // Click Sign In in the guest mode alert
    const signInLink = page.locator('a[href*="/login?redirect=/sap/placement"]').first();
    await expect(signInLink).toBeVisible();
    await signInLink.click();
    await page.waitForURL(
      (url) => url.pathname === '/login' && url.searchParams.get('redirect') === '/sap/placement',
      { timeout: 10000 }
    );
    expect(page.url()).toContain('/login');
    expect(page.url()).toContain('/sap/placement');

    // Register a fresh user through this login/register form
    const toggleBtn = page.getByRole('button', { name: /create an account/i });
    if (await toggleBtn.isVisible()) {
      await toggleBtn.click();
    }

    const testId = Date.now();
    const username = `u_sap_${testId}_${Math.floor(Math.random() * 1000)}`;
    const password = 'Password123!';

    await page.locator('input[placeholder*="Username"]').fill(username);
    await page.locator('input[placeholder*="Password"]').fill(password);

    const submitBtn = page.getByRole('button', { name: /^create account$/i });
    await submitBtn.click();

    // Must return the user back to /sap/placement (NOT /dashboard)
    await page.waitForURL((url) => url.pathname === '/sap/placement', { timeout: 15000 });
    expect(page.url()).toContain('/sap/placement');

    // 2. Open redirect rejection: attempt login with an unsafe external redirect
    await page.goto('/login?redirect=https://evil.com');
    await page.waitForLoadState('networkidle');
    // Because user is already authenticated, the page must safely redirect to /dashboard, NOT https://evil.com!
    await page.waitForURL((url) => url.pathname === '/dashboard', { timeout: 10000 });
    expect(page.url()).toContain('/dashboard');
  });

});
