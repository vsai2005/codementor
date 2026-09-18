import { test, expect, type Page } from '@playwright/test';

async function registerUser(page: Page) {
  const testId = Date.now();
  const username = `u_${testId}_${Math.floor(Math.random() * 1000)}`;
  const password = 'Password123!';

  await page.goto('/login');
  await page.waitForLoadState('networkidle');

  const toggleBtn = page.getByRole('button', { name: /create an account/i });
  if (await toggleBtn.isVisible()) {
    await toggleBtn.click();
  }

  await page.locator('input[placeholder*="Username"]').fill(username);
  await page.locator('input[placeholder*="Password"]').fill(password);

  const submitBtn = page.getByRole('button', { name: /^create account$/i });
  await submitBtn.click();

  await page.waitForURL('**/dashboard', { timeout: 25000 });
  return { username, password };
}

test.describe('SAP UX, Runtime Gating & Decoupled Roadmap E2E', () => {

  test('1. Roadmap always renders all 9 phases and Days 1-100 when curriculum loads', async ({ page }) => {
    await page.goto('/sap/learning');
    await page.waitForLoadState('networkidle');

    // Breadcrumbs & Header
    await expect(page.locator('h1')).toContainText(/S\/4HANA Enterprise Curriculum/i);

    // Verify all 9 phase navigator tabs exist
    for (let p = 1; p <= 9; p++) {
      await expect(page.getByRole('button', { name: new RegExp(`P${p}:`, 'i') })).toBeVisible();
    }

    // Verify Phase 1 active banner
    await expect(page.locator('body')).toContainText(/Phase 1 of 9/i);

    // Click Phase 2 and verify Days 9-22 milestones render
    await page.getByRole('button', { name: /P2:/i }).click();
    await expect(page.locator('body')).toContainText(/Phase 2 of 9/i);
    await expect(page.locator('body')).toContainText(/DAY 9/i);
  });

  test('2. Decoupled loading: Progress API failure does NOT hide 100-day roadmap and provides retry state', async ({ page }) => {
    // Intercept /api/sap/learning/progress and simulate a 500 server error
    await page.route('**/api/sap/learning/progress', async (route) => {
      await route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({ detail: 'Simulated Database Failure on User Progress' }),
      });
    });

    await page.goto('/sap/learning');
    await page.waitForLoadState('networkidle');

    // Curriculum must STILL be visible!
    await expect(page.locator('h1')).toContainText(/S\/4HANA Enterprise Curriculum/i);
    await expect(page.getByRole('button', { name: /P1:/i })).toBeVisible();
    await expect(page.getByRole('button', { name: /P9:/i })).toBeVisible();

    // Non-blocking progress error banner must be displayed with retry button
    await expect(page.locator('body')).toContainText(/Progress sync unavailable/i);
    const retryBtn = page.getByRole('button', { name: /Retry Progress Sync/i });
    await expect(retryBtn).toBeVisible();

    // Verify Day 1 still displays as START DAY and Day 2 as LOCKED
    await expect(page.getByRole('link', { name: /START DAY/i }).first()).toBeVisible();
    await expect(page.getByRole('button', { name: /LOCKED/i }).first()).toBeVisible();
  });

  test('3. Permanent Primary CTA: New learner sees START SAP LEARNING routing to /sap/placement', async ({ page }) => {
    // Navigate to /sap
    await page.goto('/sap');
    await page.waitForLoadState('networkidle');

    const hubCta = page.getByRole('link', { name: /START SAP LEARNING/i }).first();
    await expect(hubCta).toBeVisible();
    await expect(hubCta).toHaveAttribute('href', '/sap/placement');

    // Navigate to /sap/learning
    await page.goto('/sap/learning');
    await page.waitForLoadState('networkidle');

    const roadmapCta = page.getByRole('link', { name: /START SAP LEARNING/i }).first();
    await expect(roadmapCta).toBeVisible();
    await expect(roadmapCta).toHaveAttribute('href', '/sap/placement');
  });

  test('4. Correct per-day CTA states on unplaced / first visit (Day 1 START DAY, subsequent LOCKED)', async ({ page }) => {
    await page.goto('/sap/learning');
    await page.waitForLoadState('networkidle');

    // Day 1 has START DAY
    const day1Cta = page.getByRole('link', { name: /START DAY/i }).first();
    await expect(day1Cta).toBeVisible();
    await expect(day1Cta).toHaveAttribute('href', '/sap/learning/day/1');

    // Day 2 has LOCKED
    const lockedCta = page.getByRole('button', { name: /LOCKED/i }).first();
    await expect(lockedCta).toBeVisible();
    await expect(lockedCta).toBeDisabled();
  });

  test('5. Placed learner sees CONTINUE LEARNING — DAY X, waived days visually distinct & excluded from completed', async ({ page }) => {
    // Mock placement profile assigning start Day 4 and waiving Days 1, 2, 3
    await page.route('**/api/sap/placement/profile', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          persona: 'ABAP Developer',
          diagnostic_score: 85,
          recommended_start_day: 4,
          unlocked_days: [1, 2, 3, 4],
          waived_days: [1, 2, 3],
          rationale: 'Placed into Day 4 based on diagnostic.',
          domain_scores: { erp_architecture: 90 },
        }),
      });
    });

    await page.route('**/api/sap/learning/progress', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          course_slug: 'sap-s4hana-100',
          current_day: 4,
          completed_days: [],
          waived_days: [1, 2, 3],
          total_days: 100,
          day_states: {
            '1': { day_number: 1, lesson_completed: false, practice_completed: false, assessment_passed: false, completed: false, waived: true, unlocked: true, status: 'waived_by_placement' },
            '2': { day_number: 2, lesson_completed: false, practice_completed: false, assessment_passed: false, completed: false, waived: true, unlocked: true, status: 'waived_by_placement' },
            '3': { day_number: 3, lesson_completed: false, practice_completed: false, assessment_passed: false, completed: false, waived: true, unlocked: true, status: 'waived_by_placement' },
            '4': { day_number: 4, lesson_completed: false, practice_completed: false, assessment_passed: false, completed: false, waived: false, unlocked: true, status: 'available' },
          },
        }),
      });
    });

    await page.goto('/sap/learning');
    await page.waitForLoadState('networkidle');

    // 1. Primary CTA must show CONTINUE LEARNING — DAY 4
    const continueCta = page.getByRole('link', { name: /CONTINUE LEARNING — DAY 4/i }).first();
    await expect(continueCta).toBeVisible();
    await expect(continueCta).toHaveAttribute('href', '/sap/learning/day/4');

    // 2. Waived days must show WAIVED BY PLACEMENT badge and REVIEW DAY
    const waivedBadge = page.locator('text=WAIVED BY PLACEMENT').first();
    await expect(waivedBadge).toBeVisible();

    // 3. Completed counter must NOT count waived days as completed (0 / 100 Days)
    await expect(page.locator('body')).toContainText(/Progress:\s*0\s*\/\s*100 Days/i);
    await expect(page.locator('body')).toContainText(/\+3 waived/i);

    // 4. Day 4 must show START DAY
    const day4Cta = page.getByRole('link', { name: /START DAY/i }).first();
    await expect(day4Cta).toBeVisible();
    await expect(day4Cta).toHaveAttribute('href', '/sap/learning/day/4');
  });

  test('6. In-progress day shows CONTINUE DAY; completed day shows REVIEW DAY', async ({ page }) => {
    // Mock progress where Day 1 is completed and Day 2 has lesson in progress
    await page.route('**/api/sap/learning/progress', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          course_slug: 'sap-s4hana-100',
          current_day: 2,
          completed_days: [1],
          waived_days: [],
          total_days: 100,
          day_states: {
            '1': { day_number: 1, lesson_completed: true, practice_completed: true, assessment_passed: true, completed: true, waived: false, unlocked: true, status: 'completed' },
            '2': { day_number: 2, lesson_completed: true, practice_completed: false, assessment_passed: false, completed: false, waived: false, unlocked: true, status: 'in_progress' },
          },
        }),
      });
    });

    await page.goto('/sap/learning');
    await page.waitForLoadState('networkidle');

    // Day 1 shows REVIEW DAY
    const day1Review = page.getByRole('link', { name: /REVIEW DAY/i }).first();
    await expect(day1Review).toBeVisible();
    await expect(day1Review).toHaveAttribute('href', '/sap/learning/day/1');

    // Day 2 shows CONTINUE DAY
    const day2Continue = page.getByRole('link', { name: /CONTINUE DAY/i }).first();
    await expect(day2Continue).toBeVisible();
    await expect(day2Continue).toHaveAttribute('href', '/sap/learning/day/2');

    // Progress counter shows 1 / 100 Days
    await expect(page.locator('body')).toContainText(/Progress:\s*1\s*\/\s*100 Days/i);
  });

  test('7. SAP Missions error handling: API failure shows error banner with retry button, recovers on retry', async ({ page }) => {
    await registerUser(page);
    let failMissions = true;

    // Intercept missions API
    await page.route('**/api/sap/missions', async (route) => {
      if (failMissions) {
        await route.fulfill({
          status: 500,
          contentType: 'application/json',
          body: JSON.stringify({ detail: 'Simulated Database Failure on Missions' }),
        });
      } else {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify([
            {
              id: 'm1',
              slug: 'nm01-mat-recon',
              title: 'Material Valuation Dispute',
              mission_type: 'INCIDENT',
              difficulty: 2,
              score: 0,
              passed: false,
              attempt_status: 'NOT_STARTED',
              related_days: [1, 2],
              concept_slugs: ['plant-loc', 'val-area'],
              description: 'Resolve reconciliation differences.',
            },
          ]),
        });
      }
    });

    await page.goto('/sap/missions');
    await page.waitForLoadState('networkidle');

    // Error banner should be visible
    await expect(page.locator('body')).toContainText(/Failed to Load Missions/i);
    // Should NOT show "0 Missions Available"
    await expect(page.locator('text=0 Missions Available')).not.toBeVisible();

    const retryBtn = page.getByRole('button', { name: /Retry Loading Missions/i });
    await expect(retryBtn).toBeVisible();

    // Now make the API succeed and click retry
    failMissions = false;
    await retryBtn.click();
    await page.waitForLoadState('networkidle');

    // Should now show the mission
    await expect(page.locator('body')).toContainText(/Material Valuation Dispute/i);
    await expect(page.locator('body')).toContainText(/1 Missions Available/i);
  });

  test('8. SAP Missions valid empty state: displays No Missions Available without error banner', async ({ page }) => {
    await registerUser(page);
    await page.route('**/api/sap/missions', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([]),
      });
    });

    await page.goto('/sap/missions');
    await page.waitForLoadState('networkidle');

    await expect(page.locator('body')).toContainText(/No Missions Available/i);
    await expect(page.locator('text=Failed to Load Missions')).not.toBeVisible();
  });

  test('9. SAP Mission Detail error handling: API failure displays Failed to Load Mission with retry button', async ({ page }) => {
    await registerUser(page);
    let failDetail = true;

    await page.route('**/api/sap/missions/test-mission*', async (route) => {
      if (failDetail) {
        await route.fulfill({
          status: 500,
          contentType: 'application/json',
          body: JSON.stringify({ detail: 'Simulated Network Failure on Detail' }),
        });
      } else {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            id: 'm-test',
            slug: 'test-mission',
            title: 'Test Recovery Mission',
            description: 'A test mission for verification',
            mission_type: 'PROCESS_TASK',
            difficulty: 1,
            estimated_minutes: 15,
            enterprise_code: 'NM01',
            related_days: [1],
            concept_slugs: ['erp-basics'],
            steps: [
              {
                step_id: 's1',
                order: 1,
                title: 'Initial Investigation',
                task_description: 'Check initial conditions',
                options: [{ id: 'opt1', label: 'Execute inspection' }],
              },
            ],
          }),
        });
      }
    });

    await page.goto('/sap/missions/test-mission');
    await page.waitForLoadState('networkidle');

    // Distinct error card should be visible
    await expect(page.locator('h1')).toContainText(/Failed to Load Mission/i);
    const retryBtn = page.getByRole('button', { name: /Retry Loading/i });
    await expect(retryBtn).toBeVisible();

    // Recover on retry
    failDetail = false;
    await retryBtn.click();
    await page.waitForLoadState('networkidle');

    await expect(page.locator('h1')).toContainText(/Test Recovery Mission/i);
  });

});
