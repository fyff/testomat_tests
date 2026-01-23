# Project: testomat_tests

## Overview

This project is an automated End-to-End (E2E) testing framework for the Testomat application. It utilizes **Python**
with **Playwright** and **Pytest**.

## Tech Stack

- **Language:** Python 3.14+
- **Browser Automation:** Playwright (Sync API), pytest-playwright
- **Test Runner:** Pytest, pytest-html
- **Linting/Formatting:** Ruff
- **HTTP Client:** Httpx (for API testing)
- **Utilities:** Faker, Python-dotenv

## Architecture

### Directory Structure

- `src/` - Application Code (Automation Logic)
    - `web/` - Web Automation (UI)
        - `pages/` - Page Object Models (POM). Each file represents a specific page (e.g., `login_page.py`).
        - `components/` - Reusable UI components (e.g., `auth_header.py`).
        - `application.py` - Facade class (`Application`) that provides access to all pages/components.
    - `api/` - API Automation
        - `client.py` - `APIClient` wrapper around `httpx`.
        - `models.py` - Data models.
- `tests/` - Test Suites
    - `web/` - UI Tests.
        - `enterprise_plan_tests/` - Tests specific to the Enterprise plan.
        - `free_plan_tests/` - Tests specific to the Free plan.
    - `api/` - API Tests.
    - `fixtures/` - Pytest fixtures (`app.py`, `config.py`, `playwright.py`).
- `test-result/` - Artifacts (screenshots, traces, videos, report.html).

### Design Patterns

1. **Page Object Model (POM):**
    - Locators are defined in `__init__`.
    - Interaction methods (e.g., `login`) encapsulate logic.
    - Verification methods (e.g., `wait_for_loaded`) ensure state.
    - **Fluent Interface:** Methods often return `Self` to allow chaining (e.g., `page.open().login(...)`).
2. **Facade Pattern:**
    - The `Application` class acts as a single entry point for tests to access any page object.
3. **Fixture-Driven Tests:**
    - Setup and teardown are handled via `pytest` fixtures in `tests/fixtures/` and `conftest.py`.

## Coding Guidelines

### General

- **Type Hinting:** Strictly used. Use `typing.Self` for chainable methods.
- **Imports:** Use absolute imports (e.g., `from src.web.application import Application`).
- **Formatting:** Follow `ruff` configuration (line length 120, double quotes).

### Playwright / POM

- Initialize locators in `__init__` using `self.page.locator(...)` or `self.page.get_by_...`.
- Use `expect(...)` for assertions within Page Objects to verify state (e.g., `wait_for_loaded`).
- Avoid raw `time.sleep()`; use `expect` with timeouts or `wait_for_*` methods.

### Testing

- **Markers:** Use strictly defined markers:
    - `@pytest.mark.smoke`
    - `@pytest.mark.regression`
    - `@pytest.mark.web`
    - `@pytest.mark.slow`
- **Parametrization:** Use `pytest.mark.parametrize` with `pytest.param(..., id="...")` for clear test reporting.
- **Fixtures:**
    - `app`: New browser context, unauthenticated (good for login tests).
    - `logged_app`: Session-scoped authenticated context (reused state, fast).
    - `isolated_logged_app`: Function-scoped authenticated context (clean state, slower).
    - `free_project_app`: Authenticated context for the Free plan.

## Commands

- **Run all tests:** `pytest`
- **Run web tests:** `pytest -m web`
- **Run smoke tests:** `pytest -m smoke`
- **Run specific file:** `pytest tests/web/login_page_test.py`
- **Run with head (debug):** `pytest --headed`
- **View Report:** `open test-result/report.html` (macOS)
- **Lint:** `ruff check .`
- **Format:** `ruff format .`