import pytest
from playwright.sync_api import expect

from src.web import Application
from tests.fixtures.config import Config

TARGET_PROJECT_NAME = "python manufacture"
EMPTY_PROJECT_NAME = "Electronics, Games & Industrial"


@pytest.mark.regression
@pytest.mark.web
def test_search_project(logged_app: Application):
    dashboard = logged_app.dashboard_page
    dashboard.search_project(TARGET_PROJECT_NAME)
    expect(logged_app.page.get_by_role("heading", name=TARGET_PROJECT_NAME)).to_be_visible()


@pytest.mark.web
def test_overview_project_card_details(logged_app: Application):
    card = logged_app.dashboard_page.get_project(TARGET_PROJECT_NAME)
    card.has_title(TARGET_PROJECT_NAME)
    card.has_test_count("26 tests")
    card.has_badge("Classical")
    card.has_badge("Pytest")
    card.is_demo_project()
    card.has_team_members_count(3)
    card.has_team_overflow()


@pytest.mark.web
@pytest.mark.regression
def test_open_project(logged_app: Application, configs: Config):
    dashboard_page = logged_app.dashboard_page

    project = dashboard_page.get_project(TARGET_PROJECT_NAME)
    project.open()

    expect(logged_app.page).to_have_url(configs.app_base_url + "/projects/pythonmanufacture/")
    expect(logged_app.page.locator("#ember42")).to_be_visible()
    expect(logged_app.page.locator("#ember42")).to_have_text("Python manufacture")


@pytest.mark.smoke
@pytest.mark.web
def test_verify_subscription_plan(logged_app: Application):
    dashboard = logged_app.dashboard_page
    tooltip_text = "You have a Enterprise subscription"
    expect(dashboard.get_plan_badge).to_contain_text("Enterprise plan")
    dashboard.get_plan_badge.hover()
    expect(logged_app.page.get_by_text(tooltip_text)).to_be_visible()


@pytest.mark.web
def test_verify_empty_project_state(logged_app: Application):
    dashboard = logged_app.dashboard_page

    dashboard.search_project(EMPTY_PROJECT_NAME)
    card = dashboard.get_project(EMPTY_PROJECT_NAME)

    card.has_title(EMPTY_PROJECT_NAME)
    card.has_test_count("0 tests")
    card.has_badge("Classical")


@pytest.mark.web
def test_dashboard_grid_is_not_empty(logged_app: Application):
    dashboard = logged_app.dashboard_page
    expect(dashboard.get_project_card_locator).not_to_have_count(0)


@pytest.mark.regression
def test_create_new_project_navigation(logged_app: Application, configs: Config):
    dashboard = logged_app.dashboard_page
    dashboard.create_project()

    expect(logged_app.page).to_have_url(configs.app_base_url + "/projects/new")
    expect(logged_app.page.locator("h2")).to_have_text("New Project")


@pytest.mark.web
def test_dashboard_table_is_not_empty(logged_app: Application):
    dashboard = logged_app.dashboard_page
    dashboard.switch_to_table_view()
    expect(dashboard.get_table_rows_locator).not_to_have_count(0)


@pytest.mark.smoke
def test_switch_to_free_project(isolated_logged_app: Application):
    dashboard = isolated_logged_app.dashboard_page
    dashboard.wait_for_loaded()
    dashboard.select_company("Free Projects")

    expect(dashboard.empty_state_message).to_be_visible(timeout=5000)
    expect(dashboard.create_company_link).to_be_visible()
    expect(dashboard.no_project_image).to_be_visible()
    expect(dashboard.docs_link).to_have_attribute("href", "https://docs.testomat.io")


@pytest.mark.smoke
def test_sign_out(isolated_logged_app: Application):
    dashboard = isolated_logged_app.dashboard_page
    login = isolated_logged_app.login_page

    dashboard.wait_for_loaded()
    dashboard.auth_header.open_user_menu()
    dashboard.auth_header.sign_out()

    login.wait_for_loaded()
    expect(login.sign_out_message).to_be_visible()
    expect(login.sign_out_message).to_have_text("You must be logged in to access this page")
