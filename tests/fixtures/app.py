import json
import time
from pathlib import Path

import pytest
from playwright.sync_api import Browser, BrowserContext, Page

from src.web import Application
from tests.fixtures.config import Config
from tests.fixtures.cookie_helper import (
    CookieHelper,
    clear_browser_state,
)

STORAGE_STATE_PATH = Path("test-result/.auth/storage_state.json")
FREE_PROJECT_STORAGE_PATH = Path("test-result/.auth/free_project_state.json")
SESSION_TTL = 86400  # 1 day in seconds


def create_free_project_state() -> None:
    """Create free project state by copying storage state with empty company_id."""
    if not STORAGE_STATE_PATH.exists():
        return

    try:
        state = json.loads(STORAGE_STATE_PATH.read_text())
    except (OSError, json.JSONDecodeError):
        return

    for cookie in state.get("cookies", []):
        if cookie.get("name") == "company_id":
            cookie["value"] = ""
            break

    FREE_PROJECT_STORAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    FREE_PROJECT_STORAGE_PATH.write_text(json.dumps(state, indent=2))


def build_browser_context(
    browser: Browser,
    base_url: str | None,
    storage_state: Path | None = None,
) -> BrowserContext:
    if base_url is None:
        raise ValueError("base_url must be provided and cannot be None. Check your environment variables.")

    kwargs = {
        "base_url": base_url,
        "viewport": {"width": 1680, "height": 900},
        "locale": "en-GB",
        "timezone_id": "Europe/Kyiv",
        "record_video_dir": "test-result/videos/",
        "permissions": ["geolocation"],
    }
    if storage_state and storage_state.exists():
        kwargs["storage_state"] = str(storage_state)
    return browser.new_context(**kwargs)


def perform_login(page: Page, email: str, password: str) -> bool:
    """Performs login steps on the given page."""
    app = Application(page)
    app.login_page.open().login(email, password)
    return True


@pytest.fixture(scope="function")
def app(browser_instance: Browser, configs: Config) -> Application:
    """Provides a clean, unauthenticated application instance for each test.
    A new browser context and page are created for each test."""
    context = build_browser_context(browser_instance, configs.app_base_url)
    page = context.new_page()
    yield Application(page)
    page.close()
    context.close()


def is_logged_in(page: Page) -> bool:
    """Checks if the user is currently logged in."""
    try:
        page.goto("/projects", timeout=5000)
        # Check for a specific element that only appears when logged in, e.g., company dropdown or logout button
        return page.locator(".v-select__selection").is_visible(timeout=2000)
    except Exception:
        return False


@pytest.fixture(scope="session")
def auth_state(browser_instance: Browser, configs: Config) -> Path:
    """
    Ensures a valid authentication state exists.
    Returns the path to the storage state file.
    Uses time-based validation (TTL) to avoid unnecessary browser launches.
    """
    if STORAGE_STATE_PATH.exists():
        file_age = time.time() - STORAGE_STATE_PATH.stat().st_mtime
        if file_age < SESSION_TTL:
            return STORAGE_STATE_PATH

        STORAGE_STATE_PATH.unlink()

    context = build_browser_context(browser_instance, configs.app_base_url)
    page = context.new_page()

    try:
        perform_login(page, configs.email, configs.password)
        STORAGE_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        context.storage_state(path=STORAGE_STATE_PATH)
        create_free_project_state()
    finally:
        page.close()
        context.close()

    return STORAGE_STATE_PATH


@pytest.fixture(scope="function")
def logged_app(browser_instance: Browser, configs: Config, auth_state: Path) -> Application:
    """
    Provides a logged-in application instance for each test with its own context.
    """
    context = build_browser_context(browser_instance, configs.app_base_url, storage_state=auth_state)
    page = context.new_page()
    page.goto("/projects")
    app = Application(page)
    yield app
    page.close()
    context.close()


@pytest.fixture(scope="function")
def isolated_logged_app(browser_instance: Browser, configs: Config) -> Application:
    """
    Provides a logged-in application instance with a clean state for each test.
    It creates a new browser context and logs in for each test, ensuring no shared state.
    This is slower than `logged_app` but safer for tests that need isolation.
    """
    context = build_browser_context(browser_instance, configs.app_base_url)
    page = context.new_page()
    perform_login(page, configs.email, configs.password)
    yield Application(page)
    page.close()
    context.close()


@pytest.fixture(scope="function")
def cookies(browser_instance: Browser, configs: Config, auth_state: Path) -> CookieHelper:
    """Provides cookie manipulation helper for a fresh logged-in context."""
    context = build_browser_context(browser_instance, configs.app_base_url, storage_state=auth_state)
    yield CookieHelper(context)
    context.close()


@pytest.fixture(scope="module")
def module_page(browser_instance: Browser, configs: Config) -> Page:
    """Shared page for parametrized tests (module scope) - reuses same page across test params."""
    context = build_browser_context(browser_instance, configs.app_base_url)
    page = context.new_page()
    yield page
    page.close()
    context.close()


@pytest.fixture(scope="function")
def shared_page(module_page: Page) -> Application:
    """
    Provides an application instance that shares a single page across all tests in a module.
    The page state is cleaned after each test.
    """
    yield Application(module_page)
    clear_browser_state(module_page)


@pytest.fixture(scope="session")
def free_auth_state(configs: Config, auth_state: Path) -> Path:
    """
    Ensures a valid authentication state for free projects exists.
    We do NOT open the browser for verification because auth_state already guaranteed the session validity.
    """
    create_free_project_state()
    return FREE_PROJECT_STORAGE_PATH


@pytest.fixture(scope="function")
def free_project_app(browser_instance: Browser, configs: Config, free_auth_state: Path) -> Application:
    """Provides a logged-in application instance for Free Plan tests with its own context."""
    context = build_browser_context(browser_instance, configs.app_base_url, storage_state=free_auth_state)
    page = context.new_page()
    page.goto("/projects")
    yield Application(page)
    page.close()
    context.close()
