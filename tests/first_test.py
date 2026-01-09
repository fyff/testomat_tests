import os

import pytest
from faker import Faker
from playwright.sync_api import Page, expect

from tests.conftest import Config

TARGET_PROJECT = "python manufacture"


@pytest.fixture(scope="function")
def login(page: Page, configs: Config):
    page.goto(configs.app_base_url)
    login_user(page, configs.email, configs.password)


def test_login_with_invalid_creds(page: Page, configs: Config):
    open_home_page(page)
    page.get_by_text("Log in", exact=True).click()
    invalid_password = Faker().password(length=10)

    login_user(page, configs.email, invalid_password)

    expect(page.locator("#content-desktop").get_by_text("Invalid Email or password.")).to_be_visible()
    expect(page.locator("#content-desktop .common-flash-info")).to_have_text("Invalid Email or password.")


def test_search_project_in_company(page: Page, login):
    search_project(page, TARGET_PROJECT)
    expect(page.get_by_role("heading", name=TARGET_PROJECT)).to_be_visible()


def test_open_free_project(page: Page, login):
    page.locator("#company_id").click()
    page.locator("#company_id").select_option("Free Projects")
    search_project(page, TARGET_PROJECT)

    expect(page.get_by_role("heading", name=TARGET_PROJECT)).to_be_hidden()
    expect(page.get_by_text("You have not created any projects yet")).to_be_visible(timeout=10000)


def open_home_page(page: Page):
    page.goto(os.getenv("BASE_URL"))


def login_user(page: Page, email: str, password: str):
    page.locator("#content-desktop #user_email").fill(email)
    page.locator("#content-desktop #user_password").fill(password)
    page.get_by_role("button", name="Sign in").click()


def search_project(page: Page, target_project: str):
    expect(page.get_by_role("searchbox", name="Search")).to_be_visible()
    page.locator("#content-desktop #search").fill(target_project)
