import pytest
from playwright.sync_api import Page, expect

from src.web.pages.DashboardPage import DashboardPage
from src.web.pages.LoginPage import LoginPage
from tests.conftest import Config

TARGET_PROJECT_NAME = "python manufacture"
EMPTY_PROJECT_NAME = "Industrial"


@pytest.fixture(scope="function")
def login(page: Page, configs: Config):
    login_page = LoginPage(page)
    login_page.open()
    login_page.is_loaded()
    login_page.login(configs.email, configs.password)


def test_search_project(page: Page, login):
    dashboard = DashboardPage(page)
    dashboard.search_project(TARGET_PROJECT_NAME)
    expect(page.get_by_role("heading", name=TARGET_PROJECT_NAME)).to_be_visible()


def test_project_card_details(page: Page, login):
    card = DashboardPage(page).get_project(TARGET_PROJECT_NAME)
    card.has_title("python manufacture")
    card.has_test_count("26 tests")
    card.has_badge("Classical")
    card.has_badge("Pytest")
    card.is_demo_project()
    card.has_team_members_count(3)
    card.has_team_overflow()


def test_open_project(page: Page, login, configs: Config):
    dashboard_page = DashboardPage(page)

    project = dashboard_page.get_project(TARGET_PROJECT_NAME)
    project.open()

    expect(page).to_have_url(configs.login_url + "/projects/pythonmanufacture/")
    # TODO project_details.is_loaded(TARGET_PROJECT)


def test_verify_subscription_plan(page: Page, login):
    dashboard = DashboardPage(page)
    tooltip_text = "You have a Enterprise subscription"
    expect(dashboard.get_plan_badge).to_contain_text("Enterprise plan")
    dashboard.get_plan_badge.hover()
    expect(page.get_by_text(tooltip_text)).to_be_visible()


def test_verify_empty_project_state(page: Page, login):
    dashboard = DashboardPage(page)

    dashboard.search_project(EMPTY_PROJECT_NAME)
    card = dashboard.get_project(EMPTY_PROJECT_NAME)

    card.has_title(EMPTY_PROJECT_NAME)
    card.has_test_count("0 tests")
    card.has_badge("Classical")


def test_dashboard_grid_is_not_empty(page: Page, login):
    dashboard = DashboardPage(page)
    expect(dashboard.get_project_card_locator).not_to_have_count(0)


def test_create_new_project_navigation(page: Page, login, configs: Config):
    dashboard = DashboardPage(page)
    dashboard.create_project()

    expect(page).to_have_url(configs.login_url + "/projects/new")
    expect(page.locator("h2")).to_have_text("New Project")


def test_open_free_project(page: Page, login):
    dashboard = DashboardPage(page)
    dashboard.select_company("Free Projects")

    expect(page.get_by_text("You have not created any projects yet")).to_be_visible(timeout=10000)
