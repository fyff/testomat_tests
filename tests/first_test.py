from playwright.sync_api import Page, expect


def login_with_invalid_password(page: Page):
    page.goto("https://testomat.io/")
    page.get_by_text("Log in", exact=True).click()
    page.locator("#content-desktop #user_email").fill("soul.2fast4u@gmail.com")
    page.locator("#content-desktop #user_password").fill("1234")
    page.get_by_role(role="button", name="Sign in").click()

    expect(page.locator("#content-desktop").get_by_text("Invalid Email or password.")).to_be_visible()
    expect(page.locator("#content-desktop .common-flash-info")).to_have_text("Invalid Email or password.")