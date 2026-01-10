import os
from dataclasses import dataclass

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright, ViewportSize

from src.web.Application import Application

load_dotenv()


def clear_browser_state(page: Page) -> None:
    """Clear cookies and local storage for the current page context."""
    page.context.clear_cookies()
    page.evaluate("window.localStorage.clear()")
    page.evaluate("window.sessionStorage.clear()")


@dataclass(frozen=True)
class Config:
    base_url: str
    app_base_url: str
    email: str
    password: str


@pytest.fixture(scope="session")
def configs() -> Config:
    return Config(
        base_url=os.getenv("BASE_URL"),
        app_base_url=os.getenv("BASE_APP_URL"),
        email=os.getenv("EMAIL"),
        password=os.getenv("PASSWORD"),
    )


# Shared browser instance for session
@pytest.fixture(scope="session")
def browser_instance():
    """
    Provides a single browser instance for the entire test session.
    This is more efficient than launching a new browser for each test.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=0, timeout=30000)
        yield browser
        browser.close()


# 1. Clean app - fresh page per test (function scope)
@pytest.fixture(scope="function")
def app(browser_instance: Browser, configs: Config) -> Application:
    """
    Provides a clean, unauthenticated application instance for each test.
    A new browser context and page are created for each test, ensuring complete isolation.
    """
    context = build_browser_instance(browser_instance, configs)

    page = context.new_page()
    yield Application(page)
    page.close()
    context.close()


# 2. Logged app - reuses authenticated session (session scope)
@pytest.fixture(scope="session")
def logged_context(browser_instance: Browser, configs: Config) -> BrowserContext:
    """
    Provides a session-scoped, authenticated browser context.
    This context is logged in once at the beginning of the test session
    and reused by `logged_app` for all tests. This improves performance
    but means browser state (cookies, local storage) is shared across tests
    using `logged_app`.
    """
    context = build_browser_instance(browser_instance, configs)

    page = context.new_page()
    app = Application(page)
    app.login_page.open()
    app.login_page.is_loaded()
    app.login_page.login(configs.email, configs.password)
    page.close()
    yield context
    context.close()


@pytest.fixture(scope="function")
def logged_app(logged_context: BrowserContext, configs: Config) -> Application:
    """
    Provides a logged-in application instance for each test.
    It reuses the same browser context for all tests in a session, which is faster but means
    that the state (e.g., cookies, local storage) is shared between tests.
    """
    page = logged_context.new_page()
    page.goto(configs.app_base_url)
    yield Application(page)
    page.close()


@pytest.fixture(scope="function")
def isolated_logged_app(browser_instance: Browser, configs: Config) -> Application:
    """
    Provides a logged-in application instance with a clean state for each test.
    It creates a new browser context and logs in for each test, ensuring no shared state.
    This is slower than `logged_app` but safer for tests that need isolation.
    """
    context = build_browser_instance(browser_instance, configs)
    page = context.new_page()
    app_instance = Application(page)
    app_instance.login_page.open()
    app_instance.login_page.is_loaded()
    app_instance.login_page.login(configs.email, configs.password)
    yield app_instance
    page.close()
    context.close()


# 3. Shared page for parametrized tests (module scope) - reuses same page across test params
@pytest.fixture(scope="module")
def shared_browser(browser_instance: Browser, configs: Config) -> Page:
    context = build_browser_instance(browser_instance, configs)

    page = context.new_page()
    yield page
    page.close()
    context.close()


def build_browser_instance(browser_instance: Browser, configs: Config) -> BrowserContext:
    viewport: ViewportSize = {"width": 1366, "height": 768}
    return browser_instance.new_context(
        base_url=configs.app_base_url,
        viewport=viewport,
        locale="uk-UA",
        timezone_id="Europe/Kyiv",
        record_video_dir="test-result/videos/",
        permissions=["geolocation"],
    )


@pytest.fixture(scope="function")
def shared_page(shared_browser: Page) -> Application:
    """
    Provides an application instance that shares a single page across all tests in a module.
    The page state is cleaned after each test.
    """
    yield Application(shared_browser)
    clear_browser_state(shared_browser)
    shared_browser.reload()
