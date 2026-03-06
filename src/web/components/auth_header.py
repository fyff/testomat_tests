from typing import Self

from playwright.sync_api import Page, expect


class AuthHeader:
    def __init__(self, page: Page):
        self.page = page
        self.container = page.locator(".auth-header-nav")
        self.logo = self.container.locator(".auth-header-nav-left-logo a")

        self.dashboard_link = self.container.get_by_role("link", name="Dashboard")
        self.companies_link = self.container.get_by_role("link", name="Companies")
        self.docs_link = self.container.get_by_role("link", name="Docs")
        self.changelog_link = self.container.get_by_role("link", name="Changelog")
        self.public_api_link = self.container.get_by_role("link", name="Public API")
        self.analytics_toggle = self.container.get_by_text("Analytics", exact=True)

        self.analytics_menu = self.container.locator("#analytics-dropdown-menu")
        self.analytics_link = self.analytics_menu.get_by_role("link", name="Analytics")
        self.analytics_dashboards_link = self.analytics_menu.get_by_role("link", name="Dashboards")

        self.new_project_btn = self.container.locator("a[href='/projects/new']")
        self.global_search_btn = self.container.locator("#showGlobalSearchBtn")
        self.profile_avatar = self.container.locator("#user-menu-button")

        self.profile_menu = self.container.locator("#profile-menu")
        self.signed_email = self.profile_menu.locator(".auth-header-nav-right-dropdown-menu-block-email")
        self.my_companies_link = self.profile_menu.get_by_role("link", name="My Companies")
        self.account_link = self.profile_menu.get_by_role("link", name="Account")
        self.downloads_link = self.profile_menu.get_by_role("link", name="Downloads")
        self.trial_request_link = self.profile_menu.get_by_role("link", name="Request a Free Trial")
        self.sign_out_btn = self.profile_menu.get_by_role("button", name="Sign Out")

    def wait_for_loaded(self) -> Self:
        expect(self.container).to_be_visible()
        expect(self.logo).to_be_visible()
        expect(self.profile_avatar).to_be_visible()
        return self

    def go_to_dashboard(self):
        self.dashboard_link.click()

    def go_to_companies(self):
        self.companies_link.click()

    def open_analytics_menu(self):
        if not self.analytics_menu.is_visible():
            self.analytics_toggle.click()
            expect(self.analytics_menu).to_be_visible()

    def go_to_analytics(self):
        self.open_analytics_menu()
        self.analytics_link.click()

    def go_to_analytics_dashboards(self):
        self.open_analytics_menu()
        self.analytics_dashboards_link.click()

    def go_to_docs(self):
        self.docs_link.click()

    def go_to_changelog(self):
        self.changelog_link.click()

    def go_to_public_api(self):
        self.public_api_link.click()

    def create_new_project(self):
        self.new_project_btn.click()

    def open_global_search(self):
        self.global_search_btn.click()

    def open_user_menu(self):
        if self.profile_menu.is_hidden():
            self.profile_avatar.click()

        try:
            expect(self.profile_menu).to_be_visible(timeout=3000)
        except AssertionError:
            # Retry click if menu didn't appear (handles potential JS not ready or lost clicks)
            self.profile_avatar.click()
            expect(self.profile_menu).to_be_visible()

    def go_to_my_companies(self):
        self.open_user_menu()
        self.my_companies_link.click()

    def go_to_account_settings(self):
        self.open_user_menu()
        self.account_link.click()

    def go_to_account_files(self):
        self.open_user_menu()
        self.downloads_link.click()

    def go_to_request_trial(self):
        self.open_user_menu()
        self.trial_request_link.click()

    def sign_out(self):
        self.open_user_menu()
        self.sign_out_btn.click()
