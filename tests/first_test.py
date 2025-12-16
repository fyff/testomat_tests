from playwright.sync_api import Page, expect


def test_login_with_invalid_creds(page: Page):
    open_home_page(page)
    page.get_by_text("Log in", exact=True).click()
    login_user(page, "soul.2fast4u@gmail.com", "invalid-password")

    expect(page.locator("#content-desktop").get_by_text("Invalid Email or password.")).to_be_visible()
    expect(page.locator("#content-desktop .common-flash-info")).to_have_text("Invalid Email or password.")


def test_search_project_in_company(page: Page):
    page.goto("https://app.testomat.io/users/sign_in")
    login_user(page, "soul.2fast4u@gmail.com", "temple-harvard-paradox")
    target_project = "Artory"  # TODO rename to "python manufacture"
    search_project(page, target_project)

    expect(page.get_by_role("heading", name=target_project)).to_be_visible()
    expect(page.locator("ul li h3")).to_have_text(target_project, use_inner_text=True)


def test_open_free_project(page: Page):
    page.goto("https://app.testomat.io/users/sign_in")
    login_user(page, "soul.2fast4u@gmail.com", "temple-harvard-paradox")
    page.locator("#company_id").click()
    page.locator("#company_id").select_option("Free Projects")

    target_project = "Artory"  # TODO rename to "python manufacture"
    search_project(page, target_project)
    expect(page.get_by_role("heading", name=target_project)).to_be_hidden()
    expect(page.get_by_text("You have not created any projects yet")).to_be_visible(timeout=10000)


def open_home_page(page: Page):
    page.goto("https://testomat.io/")


def login_user(page: Page, email: str, password: str):
    page.locator("#content-desktop #user_email").fill(email)
    page.locator("#content-desktop #user_password").fill(password)
    page.get_by_role("button", name="Sign in").click()


def search_project(page: Page, target_project: str):
    expect(page.get_by_role("searchbox", name="Search")).to_be_visible()
    page.locator("#content-desktop #search").fill(target_project)
