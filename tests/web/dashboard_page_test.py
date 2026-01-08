from playwright.sync_api import expect

from src.web.Application import Application
from tests.conftest import Config

TARGET_PROJECT_NAME = "python manufacture"
EMPTY_PROJECT_NAME = "Industrial"


def test_search_project(app: Application, login):
    dashboard = app.dashboard_page
    dashboard.search_project(TARGET_PROJECT_NAME)
    expect(app.page.get_by_role("heading", name=TARGET_PROJECT_NAME)).to_be_visible()


def test_project_card_details(app: Application, login):
    card = app.dashboard_page.get_project(TARGET_PROJECT_NAME)
    card.has_title("python manufacture")
    card.has_test_count("26 tests")
    card.has_badge("Classical")
    card.has_badge("Pytest")
    card.is_demo_project()
    card.has_team_members_count(3)
    card.has_team_overflow()


def test_open_project(app: Application, login, configs: Config):
    dashboard_page = app.dashboard_page

    project = dashboard_page.get_project(TARGET_PROJECT_NAME)
    project.open()

    expect(app.page).to_have_url(configs.login_url + "/projects/pythonmanufacture/")
    # TODO project_details.is_loaded(TARGET_PROJECT)


def test_verify_subscription_plan(app: Application, login):
    dashboard = app.dashboard_page
    tooltip_text = "You have a Enterprise subscription"
    expect(dashboard.get_plan_badge).to_contain_text("Enterprise plan")
    dashboard.get_plan_badge.hover()
    expect(app.page.get_by_text(tooltip_text)).to_be_visible()


def test_verify_empty_project_state(app: Application, login):
    dashboard = app.dashboard_page

    dashboard.search_project(EMPTY_PROJECT_NAME)
    card = dashboard.get_project(EMPTY_PROJECT_NAME)

    card.has_title(EMPTY_PROJECT_NAME)
    card.has_test_count("0 tests")
    card.has_badge("Classical")


def test_dashboard_grid_is_not_empty(app: Application, login):
    dashboard = app.dashboard_page
    expect(dashboard.get_project_card_locator).not_to_have_count(0)


def test_create_new_project_navigation(app: Application, login, configs: Config):
    dashboard = app.dashboard_page
    dashboard.create_project()

    expect(app.page).to_have_url(configs.login_url + "/projects/new")
    expect(app.page.locator("h2")).to_have_text("New Project")


def test_open_free_project(app: Application, login):
    dashboard = app.dashboard_page
    dashboard.select_company("Free Projects")

    expect(app.page.get_by_text("You have not created any projects yet")).to_be_visible(timeout=10000)


def test_dashboard_table_is_not_empty(app: Application, login):
    dashboard = app.dashboard_page
    dashboard.switch_to_table_view()
    expect(dashboard.get_table_rows_locator).not_to_have_count(0)
