import { test, expect, type Page } from '@playwright/test';

// The hub is driven entirely by these endpoints, so the API is mocked and the spec needs
// no backend. Unmocked /api calls are answered 401, i.e. a signed-out visitor.
const json = (body: unknown, status = 200) => ({
  status,
  contentType: 'application/json',
  body: JSON.stringify(body),
});

const sapProgress = (over: Record<string, unknown> = {}) => ({
  course_slug: 'sap-s4hana',
  current_day: 1,
  completed_days: [],
  waived_days: [],
  total_days: 100,
  day_states: {},
  ...over,
});

async function mockApi(
  page: Page,
  opts: {
    python?: { current_day: number; completed_days: number[] };
    sap?: Record<string, unknown>;
  } = {},
) {
  await page.route('**/api/**', async (route) => {
    const url = new URL(route.request().url());
    if (url.pathname === '/api/learning/progress' && opts.python) {
      return route.fulfill(json({ ...opts.python, total_days: 160, day_states: {} }));
    }
    if (url.pathname === '/api/sap/learning/progress' && opts.sap) {
      return route.fulfill(json(opts.sap));
    }
    return route.fulfill(json({ detail: 'Not authenticated' }, 401));
  });
}

const card = (page: Page, id: 'python-dsa' | 'sap-s4hana') => page.getByTestId(`course-card-${id}`);

test.describe('Unified Learning Hub', () => {
  test('navbar has exactly one Learning entry and no separate SAP entry', async ({ page }) => {
    await mockApi(page);
    await page.goto('/learning');
    const nav = page.getByRole('navigation', { name: 'Main' });
    await expect(nav.getByRole('link', { name: 'Learning', exact: true })).toHaveCount(1);
    await expect(nav.getByRole('link', { name: 'SAP', exact: true })).toHaveCount(0);
    await expect(nav.getByRole('link', { name: 'Learning', exact: true })).toHaveAttribute('aria-current', 'page');
  });

  test('signed-out visitor sees both courses with Start actions', async ({ page }) => {
    await mockApi(page);
    await page.goto('/learning');

    await expect(card(page, 'python-dsa')).toContainText('Python + DSA');
    await expect(card(page, 'sap-s4hana')).toContainText('SAP S/4HANA');

    await expect(page.getByTestId('course-card-python-dsa-progress')).toHaveText('0 of 160 days completed');
    await expect(page.getByTestId('course-card-sap-s4hana-progress')).toHaveText('0 of 100 days completed');

    const pyStart = page.getByTestId('course-card-python-dsa-primary');
    await expect(pyStart).toHaveText(/Start course/);
    await expect(pyStart).toHaveAttribute('href', '/learning/day/1');

    const sapStart = page.getByTestId('course-card-sap-s4hana-primary');
    await expect(sapStart).toHaveText(/Start course/);
    await expect(sapStart).toHaveAttribute('href', '/sap/placement');
  });

  test('in-progress learner sees progress, current day and Continue actions', async ({ page }) => {
    await mockApi(page, {
      python: { current_day: 13, completed_days: Array.from({ length: 12 }, (_, i) => i + 1) },
      sap: sapProgress({ current_day: 7, completed_days: [1, 2, 3, 4, 5, 6] }),
    });
    await page.goto('/learning');

    await expect(page.getByTestId('course-card-python-dsa-progress')).toHaveText('12 of 160 days completed');
    await expect(page.getByTestId('course-card-python-dsa-current')).toContainText('Current: Day 13');
    const pyContinue = page.getByTestId('course-card-python-dsa-primary');
    await expect(pyContinue).toContainText('Continue — Day 13');
    await expect(pyContinue).toHaveAttribute('href', '/learning/day/13');

    await expect(page.getByTestId('course-card-sap-s4hana-progress')).toHaveText('6 of 100 days completed');
    const sapContinue = page.getByTestId('course-card-sap-s4hana-primary');
    await expect(sapContinue).toContainText('Continue — Day 7');
    await expect(sapContinue).toHaveAttribute('href', '/sap/learning/day/7');

    await expect(card(page, 'python-dsa').getByRole('progressbar')).toHaveAttribute('aria-valuenow', '8');
    await expect(card(page, 'sap-s4hana').getByRole('progressbar')).toHaveAttribute('aria-valuenow', '6');
  });

  test('existing course flows are preserved behind the hub', async ({ page }) => {
    await mockApi(page);
    await page.goto('/learning');

    await page.getByTestId('course-card-python-dsa-secondary').click();
    await expect(page).toHaveURL(/\/learning\/python$/);

    await page.goto('/learning');
    await page.getByTestId('course-card-sap-s4hana-secondary').click();
    await expect(page).toHaveURL(/\/sap$/);

    // The SAP pages still highlight the single Learning nav entry.
    const nav = page.getByRole('navigation', { name: 'Main' });
    await expect(nav.getByRole('link', { name: 'Learning', exact: true })).toHaveAttribute('aria-current', 'page');
  });
});
