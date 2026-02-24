import pytest
from faker import Faker
from playwright.sync_api import expect

from src.web import Application


@pytest.mark.web
def test_overview_elements(logged_app: Application):
    create_project = logged_app.create_project_page
    create_project.open()
    create_project.wait_for_loaded()
    logged_app.auth_header.wait_for_loaded()
    logged_app.crisp_chat.wait_for_loaded()


@pytest.mark.web
def test_navigate_how_to_start(logged_app: Application):
    create_project = logged_app.create_project_page
    create_project.open()
    with logged_app.page.expect_popup() as page_info:
        create_project.click_how_to_start()
    new_page = page_info.value
    expect(new_page).to_have_url("https://docs.testomat.io/getting-started/")
    new_page.close()
    create_project.wait_for_loaded()


@pytest.mark.skip
@pytest.mark.regression
def test_create_create_project(logged_app: Application):
    target_project_name = Faker().company()

    (logged_app.create_project_page.open().fill_project_title(target_project_name).click_create())

    (logged_app.new_project_details_page.wait_for_loaded().empty_project_name_is(target_project_name).close_readme())

    (logged_app.new_project_details_page.side_bar.open().wait_for_loaded())


@pytest.mark.order(1)
@pytest.mark.smoke
@pytest.mark.regression
def test_create_suite_in_new_project(logged_app: Application):
    project_name = Faker().company()
    suite_name = Faker().word()

    logged_app.create_project_page.open()
    logged_app.create_project_page.fill_project_title(project_name)
    logged_app.create_project_page.click_create()

    project_page = logged_app.new_project_details_page.wait_for_loaded().close_readme().create_first_suite(suite_name)

    project_page.verify_project_loaded(project_name)
    project_page.verify_suite_present(suite_name)
