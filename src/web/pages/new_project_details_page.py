from typing import Self

from playwright.sync_api import Page, expect

from src.web.components.side_bar import SideBar


class NewProjectDetailsPage:
    def __init__(self, page: Page):
        self.page = page
        self.side_bar = SideBar(page)

        # Header
        self.project_title = page.locator(".sticky-header h2")
        self.readme_button = page.get_by_role("link", name="Readme")
        self.more_options_button = page.locator(".ember-basic-dropdown-trigger")

        # Manual Tests Section
        self.suite_input = page.get_by_placeholder("First Suite")
        self.add_suite_button = page.get_by_role("button", name="Suite")
        self.add_folder_button = page.get_by_role("button", name="Folder")
        self.how_to_start_link = page.get_by_role("link", name="How to start project from scratch")
        self.import_from_source_button = page.get_by_role("link", name="Import Tests from Source Code")
        self.how_to_import_code_link = page.get_by_role("link", name="How to import tests from code")
        self.import_from_testrail_button = page.get_by_role("link", name="Import from TestRail")
        self.import_from_spreadsheet_button = page.get_by_role("link", name="Import from Spreadsheet")
        # Notifications & Errors
        self.toast_notification = page.locator(".ember-notify p")

    def wait_for_loaded(self) -> Self:
        expect(self.project_title).to_be_visible()
        expect(self.suite_input).to_be_visible()
        expect(self.add_suite_button).to_be_visible()
        self.side_bar.wait_for_loaded()
        return self

    def verify_project_name(self, expected_name: str) -> Self:
        expect(self.project_title).to_have_text(expected_name)
        return self

    def close_readme(self) -> Self:
        self.page.locator(".back .third-btn").click()
        return self

    def create_first_suite(self, suite_name: str) -> Self:
        self.suite_input.fill(suite_name)
        self.add_suite_button.click()
        return self

    def create_first_folder(self, folder_name: str) -> Self:
        self.suite_input.fill(folder_name)
        self.add_folder_button.click()
        return self

    def click_add_suite(self) -> Self:
        self.add_suite_button.click()
        return self

    def click_add_folder(self) -> Self:
        self.add_folder_button.click()
        return self

    def verify_empty_title_error(self) -> Self:
        expect(self.toast_notification).to_be_visible()
        expect(self.toast_notification).to_have_text("Title shouldn't be empty")
        expect(self.toast_notification).to_be_hidden(timeout=5000)
        expect(self.suite_input).to_be_visible()
        return self

    def open_import_from_source(self):
        self.import_from_source_button.click()
        # return ImportSourcePage(self.page).wait_for_loaded()
        return self
