from faker import Faker
from playwright.sync_api import Page

from src.web.pages.NewProjectPage import NewProjectPage
from src.web.pages.ProjectDeatilsPage import ProjectDeatilsPage


def test_overview_elements(page: Page, login):
    new_project = NewProjectPage(page)
    new_project.open()
    new_project.is_loaded()

def test_navigate_how_to_start(page: Page, login):
    new_project = NewProjectPage(page)
    new_project.open()
    new_project.click_how_to_start()

def test_create_new_project(page: Page, login):
    new_project = NewProjectPage(page).open().is_loaded()
    project_details_page = ProjectDeatilsPage(page)
    target_project_name = Faker().sentence()

    new_project.fill_project_title(target_project_name)
    new_project.click_create()
    project_details_page.is_loaded()
