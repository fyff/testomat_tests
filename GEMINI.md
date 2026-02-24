# Testomat Tests Project Context

## Project Overview

`testomat_tests` is a Python-based End-to-End (E2E) testing framework for the Testomat application. It employs *
*Playwright** for web automation and **Pytest** as the test runner. **Selenium** dependencies are present for specific
legacy or complementary testing requirements.

## Key Technologies

* **Language:** Python (>=3.14)
* **Test Runner:** [Pytest](https://docs.pytest.org/)
* **Web Automation:** [Playwright](https://playwright.dev/python/) (primary), Selenium (secondary)
* **Linting & Formatting:** [Ruff](https://docs.astral.sh/ruff/)
* **Reporting:** [Allure Report](https://allurereport.org/)
* **Dependency Management:** `uv`
* **Build System:** Hatchling

## Directory Structure

* `src/` - Framework source code.
    * `web/` - Page Object Model (POM) implementation.
        * `application.py` - `Application` class; central access point for page objects and components.
        * `pages/` - Page object classes.
        * `components/` - Shared UI component classes.
    * `api/` - API client and models.
* `tests/` - Test suites.
    * `web/` - Web UI tests.
    * `api/` - API tests.
    * `fixtures/` - Pytest fixtures.
* `.github/workflows/` - CI/CD GitHub Actions configurations.
* `test-result/` - Test artifact storage (ignored by Git).

## Setup & Usage

### Prerequisites

Python 3.14+ and `uv` are required.

### Commands

* **Install dependencies:**
  ```bash
  uv sync
  ```

* **Run all tests:**
  ```bash
  uv run pytest
  ```

* **Run specific tests (e.g., smoke tests):**
  ```bash
  uv run pytest -m smoke
  ```
  (Modify `-m smoke` for other markers or specify a file path, e.g., `tests/web/login_page_test.py`)

* **Check code quality (linting):**
  ```bash
  uv run ruff check .
  ```

* **Format code:**
  ```bash
  uv run ruff format .
  ```

## Architecture

### Design Patterns

1. **Page Object Model (POM):**
    * **Locator Definition:** Locators are defined in the `__init__` method of Page Object classes using
      `self.page.locator(...)` or `self.page.get_by_...` methods.
    * **Interaction Methods:** Encapsulate user interaction logic (e.g., `login(username, password)`).
    * **Verification Methods:** Ensure page state or element visibility (e.g., `wait_for_loaded()`).
    * **Fluent Interface:** Interaction methods return `Self` (the Page Object instance) to enable method chaining (
      e.g., `page.open().login(...)`).

2. **Facade Pattern:**
    * The `Application` class (`src/web/application.py`) functions as a facade, providing a unified and simplified
      interface for tests to interact with all page objects and components.

3. **Fixture-Driven Tests:**
    * Test setup, teardown, and resource provisioning are managed declaratively using `pytest` fixtures, primarily
      defined in `tests/fixtures/` and `tests/conftest.py`.

## Coding Guidelines

### General

* **Type Hinting:** Strictly enforced. Utilize `typing.Self` for methods implementing a fluent interface.
* **Imports:** Employ absolute imports (e.g., `from src.web.application import Application`).
* **Formatting:** Adhere to `ruff` configurations specified in `pyproject.toml` (e.g., line length 120, double quotes).

### Playwright / Page Object Model Specifics

* **Automation Driver Preference:** Playwright is the default automation driver. Selenium is reserved for existing tests
  or scenarios where Playwright is not applicable.
* **`Application` Instance Usage:** Tests must obtain page objects through the `app` fixture (an instance of
  `src.web.Application`). Direct instantiation of page objects within tests is prohibited.
* **Locator Initialization:** Locators within page objects should be initialized in the `__init__` method using
  Playwright's `locator` or `get_by_*` methods.
* **Assertions:** Prefer `expect(...)` with appropriate matchers and timeouts for assertions within Page Objects to
  verify state and element conditions.
* **Waiting:** Leverage Playwright's automatic waiting. Explicit waits should use Playwright's `wait_for_*` methods or
  `expect` with timeouts. Avoid `time.sleep()`.
* **Fixtures (from `tests/fixtures/app.py`):**
    * **Purpose:** Pytest fixtures in `tests/fixtures/app.py` manage the lifecycle of Playwright browser contexts,
      pages, authentication states, and test artifacts (traces, videos). They provide various `Application` instances
      tailored for specific testing scenarios.
    * **Authentication Management (`auth_state`):**
        * The `auth_state` fixture (session-scoped) manages Playwright's browser `storage_state`. It performs a login
          operation once per test session if no valid `storage_state.json` (at `test-result/.auth/storage_state.json`)
          exists or if it has expired (TTL 24 hours). This optimizes login time for authenticated tests.
        * `create_free_project_state()`: A utility function that derives a `free_project_state.json` from the
          authenticated state, used for testing free-plan functionalities.
    * **Browser Context and Page Provisioning:**
        * `build_browser_context()`: A helper function that configures a Playwright `BrowserContext` with base URL,
          viewport settings, locale, timezone, permissions, and optionally loads a `storage_state`. Video recording is
          enabled for non-CI runs.
        * `cleanup_artifacts()`: A context manager that ensures proper closure of Playwright pages and contexts,
          stopping tracing, and handling video and trace artifact retention based on test outcome.
    * **Application Instances:**
        * `app` (function-scoped): Provides a clean, unauthenticated `Application` instance for each test. A new browser
          context and page are created.
        * `logged_app` (function-scoped): Provides an `Application` instance with a logged-in state, utilizing the
          session-scoped `auth_state`. Each test receives its own isolated context derived from the authenticated state.
        * `isolated_logged_app` (function-scoped): Provides a logged-in `Application` instance, performing a fresh login
          for *each* test. This ensures maximum test isolation at the cost of execution time.
        * `free_project_app` (function-scoped): Provides a logged-in `Application` instance configured for free-plan
          scenarios, using `free_auth_state`.
        * `shared_page` (function-scoped): Provides an `Application` instance that shares a single Playwright `Page`
          across all tests within a module, leveraging `module_page`. This can be used for performance-sensitive tests
          where page state needs to be reset between tests (`clear_browser_state`).
    * **Artifact Handling:**
        * Tracing: Playwright tracing is started for each context (`context.tracing.start()`) and artifacts (`.zip`
          files) are saved to `test-result/traces/` on test failure by `finalize_trace_artifact()`.
        * Video Recording: Videos are recorded for non-CI runs and saved to `test-result/videos/` on test failure by
          `finalize_video_artifact()`.
    * **`cookies` (function-scoped):** Provides a `CookieHelper` instance for direct manipulation of browser cookies
      within a fresh logged-in context, useful for specific cookie-related test cases.

## CI Pipeline (GitHub Actions)

The CI pipeline, defined in `.github/workflows/tests.yml`, automates the testing workflow:

* **Triggers:** Executes on `pull_request` to `main`, a daily `schedule` (Mon-Fri, 8 AM UTC), or manual
  `workflow_dispatch` with suite selection options (`smoke`, `web`, `regression`, `all`).
* **Jobs:**
    * **`lint`:** Executes Ruff linting and formatting checks.
    * **`smoke-tests`:** Runs tests marked with `smoke`. This job is a dependency for `regression-tests`.
    * **`regression-tests`:** Executes tests marked with `regression`, conditional on `smoke-tests` completion or
      explicit `workflow_dispatch` input.
    * **`publish-report`:**
        * Downloads Allure results.
        * Generates Allure HTML reports.
        * Deploys reports to GitHub Pages.
* **Artifacts:** Playwright traces and Allure results are uploaded as artifacts on test failure for diagnostic purposes.
* **Environment Variables:** Sensitive data, including `BASE_URL`, `EMAIL`, `PASSWORD`, and `TESTOMAT_TOKEN`, are
  managed via GitHub Secrets.