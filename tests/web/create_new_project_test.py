from faker import Faker
from playwright.sync_api import Page

from src.web.Application import Application


def test_overview_elements(app: Application, login):
    new_project = app.new_project_page
    new_project.open()
    new_project.is_loaded()


def test_navigate_how_to_start(app: Application, login):
    new_project = app.new_project_page
    new_project.open()
    new_project.click_how_to_start()


def test_create_new_project(page: Page, login, app: Application):
    target_project_name = Faker().company()

    (app.new_project_page
     .open()
     .is_loaded()
     .fill_project_title(target_project_name)
     .click_create())

    (app.project_details_page
     .is_loaded()
     .empty_project_name_is(target_project_name)
     .close_readme())

    (app.project_details_page.side_bar
     .open()
     .is_loaded())
