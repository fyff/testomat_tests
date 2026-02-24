import contextlib
import json
import os
import time
from pathlib import Path

import allure
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
SESSION_TTL = 86400

IS_CI = os.getenv("CI", "false").lower() == "true"

TRACE_OPTIONS = {
    "screenshots": True,
    "snapshots": True,
    "sources": True,
}


def is_test_failed(request: pytest.FixtureRequest) -> bool:
    """Check if any test phase (setup, call, or teardown) failed."""
    setup_failed = getattr(request.node, "rep_setup", None) and request.node.rep_setup.failed
    call_failed = getattr(request.node, "rep_call", None) and request.node.rep_call.failed
    teardown_failed = getattr(request.node, "rep_teardown", None) and request.node.rep_teardown.failed
    return bool(setup_failed or call_failed or teardown_failed)


def finalize_video_artifact(video_path: str, request: pytest.FixtureRequest) -> None:
    """Saves video if test failed, otherwise deletes it."""
    if not video_path or not os.path.exists(video_path):
        return

    if not is_test_failed(request):
        with contextlib.suppress(OSError):
            os.remove(video_path)
    else:
        video_dir = Path(video_path).parent
        new_video_path = video_dir / f"{request.node.name}.webm"

        with contextlib.suppress(OSError):
            os.rename(video_path, new_video_path)


def finalize_trace_artifact(context: BrowserContext, request: pytest.FixtureRequest) -> None:
    """Stops tracing and saves it if the test failed."""
    if is_test_failed(request):
        trace_dir = Path("test-result/traces")
        trace_dir.mkdir(parents=True, exist_ok=True)
        trace_path = trace_dir / f"{request.node.name}.zip"
        with contextlib.suppress(Exception):
            context.tracing.stop(path=str(trace_path))
    else:
        with contextlib.suppress(Exception):
            context.tracing.stop()


@contextlib.contextmanager
def cleanup_artifacts(context: BrowserContext, page: Page, request: pytest.FixtureRequest):
    """Context manager to handle trace and video cleanup after test execution."""
    try:
        yield
    finally:
        video_path = ""
        with contextlib.suppress(Exception):
            if page.video:
                video_path = page.video.path()

        finalize_trace_artifact(context, request)

        page.close()
        context.close()

        if video_path:
            finalize_video_artifact(video_path, request)


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
    record_video: bool = True,
) -> BrowserContext:
    if base_url is None:
        raise ValueError("base_url must be provided and cannot be None. Check your environment variables.")

    kwargs: dict = {
        "base_url": base_url,
        "viewport": {"width": 1680, "height": 900},
        "locale": "en-GB",
        "timezone_id": "Europe/Kyiv",
        "permissions": ["geolocation"],
    }

    if storage_state and storage_state.exists():
        kwargs["storage_state"] = str(storage_state)

    if not IS_CI and record_video:
        kwargs["record_video_dir"] = "test-result/videos/"

    return browser.new_context(**kwargs)


def perform_login(page: Page, email: str, password: str) -> bool:
    """Performs login steps on the given page."""
    app = Application(page)
    app.login_page.open().login(email, password)
    return True


@pytest.fixture(scope="function")
def app(browser_instance: Browser, configs: Config, request: pytest.FixtureRequest) -> Application:
    """Provides a clean, unauthenticated application instance for each test."""
    context = build_browser_context(browser_instance, configs.app_base_url)
    context.tracing.start(**TRACE_OPTIONS)
    page = context.new_page()

    with cleanup_artifacts(context, page, request):
        yield Application(page)


@pytest.fixture(scope="session")
def auth_state(browser_instance: Browser, configs: Config) -> Path:
    """Ensures a valid authentication state exists without recording video."""
    if STORAGE_STATE_PATH.exists():
        file_age = time.time() - STORAGE_STATE_PATH.stat().st_mtime
        if file_age < SESSION_TTL:
            return STORAGE_STATE_PATH
        STORAGE_STATE_PATH.unlink()

    context = build_browser_context(browser_instance, configs.app_base_url, record_video=False)
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
def logged_app(
    browser_instance: Browser, configs: Config, auth_state: Path, request: pytest.FixtureRequest
) -> Application:
    """Provides a logged-in application instance for each test with its own context."""
    context = build_browser_context(browser_instance, configs.app_base_url, storage_state=auth_state)
    context.tracing.start(**TRACE_OPTIONS)
    page = context.new_page()
    page.goto("/projects")

    with cleanup_artifacts(context, page, request):
        yield Application(page)


@pytest.fixture(scope="function")
def isolated_logged_app(browser_instance: Browser, configs: Config, request: pytest.FixtureRequest) -> Application:
    """Provides a logged-in application instance with a clean state for each test."""
    context = build_browser_context(browser_instance, configs.app_base_url)
    context.tracing.start(**TRACE_OPTIONS)
    page = context.new_page()
    perform_login(page, configs.email, configs.password)

    with cleanup_artifacts(context, page, request):
        yield Application(page)


@pytest.fixture(scope="function")
def free_project_app(
    browser_instance: Browser, configs: Config, free_auth_state: Path, request: pytest.FixtureRequest
) -> Application:
    """Provides a logged-in application instance for Free Plan tests with its own context."""
    context = build_browser_context(browser_instance, configs.app_base_url, storage_state=free_auth_state)
    context.tracing.start(**TRACE_OPTIONS)
    page = context.new_page()
    page.goto("/projects")

    with cleanup_artifacts(context, page, request):
        yield Application(page)


@pytest.fixture(scope="function")
def cookies(browser_instance: Browser, configs: Config, auth_state: Path) -> CookieHelper:
    """Provides cookie manipulation helper for a fresh logged-in context."""
    context = build_browser_context(
        browser_instance, configs.app_base_url, storage_state=auth_state, record_video=False
    )
    yield CookieHelper(context)
    context.close()


@pytest.fixture(scope="module")
def module_page(browser_instance: Browser, configs: Config) -> Page:
    """Shared page for parametrized tests (module scope) - reuses same page across test params."""
    context = build_browser_context(browser_instance, configs.app_base_url, record_video=False)
    page = context.new_page()
    yield page
    page.close()
    context.close()


@pytest.fixture(scope="function")
def shared_page(module_page: Page) -> Application:
    """Provides an application instance that shares a single page across all tests in a module."""
    yield Application(module_page)
    clear_browser_state(module_page)


@pytest.fixture(scope="session")
def free_auth_state(configs: Config, auth_state: Path) -> Path:
    """Ensures a valid authentication state for free projects exists."""
    create_free_project_state()
    return FREE_PROJECT_STORAGE_PATH
