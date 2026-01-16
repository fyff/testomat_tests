import json
from pathlib import Path

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, expect

from src.web.application import Application
from tests.fixtures.config import Config
from tests.fixtures.cookie_helper import (
    CookieHelper,
    clear_browser_state,
)

STORAGE_STATE_PATH = Path("test-result/.auth/storage_state.json")
FREE_PROJECT_STORAGE_PATH = Path("test-result/.auth/free_project_state.json")


def create_free_project_state() -> None:
    """Create free project state by copying storage state with empty company_id."""
    if not STORAGE_STATE_PATH.exists():
        return

    state = json.loads(STORAGE_STATE_PATH.read_text())
    for cookie in state.get("cookies", []):
        if cookie.get("name") == "company_id":
            cookie["value"] = ""
            break

    FREE_PROJECT_STORAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    FREE_PROJECT_STORAGE_PATH.write_text(json.dumps(state, indent=2))


def build_browser_context(
        browser: Browser,
        base_url: str,
        storage_state: Path | None = None,
) -> BrowserContext:
    kwargs = {
        "base_url": base_url,
        "viewport": {"width": 1366, "height": 768},
        "locale": "uk-UA",
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
    app.login_page.open()
    app.login_page.is_loaded()
    app.login_page.login_user(email, password)
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


@pytest.fixture(scope="session")
def logged_page(browser_instance: Browser, configs: Config) -> BrowserContext:
    """
    Provides a session-scoped, authenticated browser context.
    This context is logged in once at the beginning of the test session
    and reused by `logged_app` for all tests. This improves performance
    but means browser state (cookies, local storage) is shared across tests
    using `logged_app`.
    """
    if STORAGE_STATE_PATH.exists():
        context = build_browser_context(browser_instance, configs.app_base_url, storage_state=STORAGE_STATE_PATH)
        yield context
        context.close()
        return

    context = build_browser_context(browser_instance, configs.app_base_url)
    page = context.new_page()
    perform_login(page, configs.email, configs.password)

    STORAGE_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    context.storage_state(path=STORAGE_STATE_PATH)
    create_free_project_state()

    yield context
    context.close()


@pytest.fixture(scope="function")
def logged_app(logged_page: BrowserContext) -> Application:
    """
    Provides a logged-in application instance for each test.
    It reuses the same browser context for all tests in a session, which is faster but means
    that the state (e.g., cookies, local storage) is shared between tests.
    """
    page = logged_page.new_page()
    page.goto("/projects")
    yield Application(page)
    page.close()


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
def cookies(logged_page: BrowserContext) -> CookieHelper:
    """Provides cookie manipulation helper for the logged-in context."""
    return CookieHelper(logged_page)


@pytest.fixture(scope="module")
def shared_browser(browser_instance: Browser, configs: Config) -> Page:
    """Shared page for parametrized tests (module scope) - reuses same page across test params."""
    context = build_browser_context(browser_instance, configs.app_base_url)
    page = context.new_page()
    yield page
    page.close()
    context.close()


@pytest.fixture(scope="function")
def shared_page(shared_browser: Page) -> Application:
    """
    Provides an application instance that shares a single page across all tests in a module.
    The page state is cleaned after each test.
    """
    yield Application(shared_browser)
    clear_browser_state(shared_browser)


@pytest.fixture(scope="session")
def free_project_page(browser_instance: Browser, configs: Config) -> Page:
    if FREE_PROJECT_STORAGE_PATH.exists():
        context = build_browser_context(browser_instance, configs.app_base_url, storage_state=FREE_PROJECT_STORAGE_PATH)
        yield context.new_page()
        context.close()
        return

    context = build_browser_context(browser_instance, configs.app_base_url)
    page = context.new_page()
    perform_login(page, configs.email, configs.password)

    app = Application(page)
    app.projects_page.is_loaded()
    app.projects_page.open()
    app.projects_page.header.select_company("Free Projects")
    expect(app.projects_page.header.free_plan_label).to_be_visible()

    FREE_PROJECT_STORAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    context.storage_state(path=FREE_PROJECT_STORAGE_PATH)

    yield page
    context.close()


@pytest.fixture(scope="function")
def free_project_app(free_project_page: Page) -> Application:
    free_project_page.goto("/projects")
    yield Application(free_project_page)
    free_project_page.close()
