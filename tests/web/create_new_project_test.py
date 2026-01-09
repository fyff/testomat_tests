from faker import Faker

from src.web.Application import Application


def test_overview_elements(logged_app: Application):
    new_project = logged_app.new_project_page
    new_project.open()
    new_project.is_loaded()


def test_navigate_how_to_start(logged_app: Application):
    new_project = logged_app.new_project_page
    new_project.open()
    new_project.click_how_to_start()


def test_create_new_project(logged_app: Application):
    target_project_name = Faker().company()

    (logged_app.new_project_page
     .open()
     .is_loaded()
     .fill_project_title(target_project_name)
     .click_create())

    (logged_app.project_details_page
     .is_loaded()
     .empty_project_name_is(target_project_name)
     .close_readme())

    (logged_app.project_details_page.side_bar
     .open()
     .is_loaded())
