from typing import Self

from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.container = page.locator("#content-desktop")
        self.form = self.container.locator("#new_user")
        self.header = self.container.get_by_role("heading", name="Sign In")
        self.sign_up_link = self.container.get_by_role("link", name="Sign Up 🚀")

        self.email_input = self.form.locator("#user_email")
        self.password_input = self.form.locator("#user_password")
        self.remember_me_checkbox = self.form.locator("#user_remember_me")
        self.sign_in_button = self.form.get_by_role("button", name="Sign In")
        self.forgot_password_link = self.form.get_by_role("link", name="Forgot your password?")

        self.google_auth_button = self.container.get_by_role("link", name="Google")
        self.github_auth_button = self.container.get_by_role("link", name="GitHub")
        self.sso_auth_button = self.container.get_by_role("link", name="SSO")

        self.sign_out_message = self.container.locator(".common-flash-info-right")

    def open(self) -> Self:
        self.page.goto("/users/sign_in")
        return self.wait_for_loaded()

    def wait_for_loaded(self) -> Self:
        expect(self.header).to_be_visible()
        expect(self.email_input).to_be_visible()
        expect(self.sign_in_button).to_be_visible()
        return self

    def login(self, email: str, password: str, remember_me: bool = False):
        self.email_input.fill(email)
        self.password_input.fill(password)

        if remember_me:
            self.remember_me_checkbox.check()

        self.sign_in_button.click()

    def invalid_login_message_visible(self):
        expect(self.container.get_by_text("Invalid Email or password.")).to_be_visible()
