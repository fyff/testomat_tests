from typing import Self

from playwright.sync_api import Page, expect

from src.web.pages.login_page import LoginPage


class LandingPage:
    def __init__(self, page: Page):
        self.page = page

    def open(self) -> Self:
        self.page.goto("https://testomat.io")
        return self.wait_for_loaded()

    def wait_for_loaded(self) -> Self:
        expect(self.page.locator("#headerMenuWrapper")).to_be_visible()
        expect(self.page.locator(".side-menu .login-item")).to_have_text("Log in")
        expect(self.page.locator(".side-menu .start-item")).to_have_text("Start for free")
        return self

    def click_login(self) -> LoginPage:
        self.page.locator(".side-menu .login-item").click()
        return LoginPage(self.page).wait_for_loaded()
