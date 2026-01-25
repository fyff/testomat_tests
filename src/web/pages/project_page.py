from typing import Self

from playwright.sync_api import Page, expect

from src.web.components.side_bar import SideBar


class SelectSuiteModal:
    def __init__(self, page: Page):
        self.page = page
        self.container = page.locator(".ember-modal-dialog")
        self.title = self.container.get_by_role("heading", name="Select suite for test")
        self.search_input = self.container.get_by_placeholder("Search suite by title")
        self.tree_list = self.container.locator(".tree-branch")
        self.select_button = self.container.get_by_role("button", name="Select")
        self.cancel_button = self.container.get_by_role("button", name="Cancel")

    def wait_for_loaded(self) -> Self:
        expect(self.container).to_be_visible()
        expect(self.title).to_be_visible()
        return self

    def search_suite(self, suite_name: str) -> Self:
        self.search_input.fill(suite_name)
        return self

    def select_suite(self, suite_name: str) -> Self:
        suite_item = self.tree_list.locator("li", has_text=suite_name).filter(
            has=self.page.locator("input[type='checkbox']")
        )
        suite_item.click()
        return self

    def click_select(self) -> ProjectPage:
        self.select_button.click()
        return ProjectPage(self.page).wait_for_loaded()

    def click_cancel(self) -> ProjectPage:
        self.cancel_button.click()
        return ProjectPage(self.page).wait_for_loaded()


class CreateSuiteModal:
    def __init__(self, page: Page):
        self.page = page
        self.container = page.locator(".detail-view-resizable")
        self.header = self.container.locator("h3")
        self.title_input = self.container.get_by_placeholder("Title")
        self.save_button = self.container.get_by_role("button", name="Save")
        self.cancel_button = self.container.get_by_role("link", name="Cancel")

    def wait_for_loaded(self, is_folder: bool = True) -> Self:
        expect(self.container).to_be_visible()
        expected_title = "New Folder" if is_folder else "New Suite"
        expect(self.header).to_have_text(expected_title)
        return self

    def fill_title(self, title: str) -> Self:
        self.title_input.fill(title)
        return self

    def click_save(self) -> ProjectPage:
        self.save_button.click()
        return ProjectPage(self.page)


class CreateTestsFromRequirementModal:
    def __init__(self, page: Page):
        self.page = page
        self.container = page.locator(".ember-modal-dialog").filter(has_text="Create Tests from Requirement")
        self.title = self.container.locator("h3")
        self.close_button = self.container.locator("button:has(.md-icon-close)")
        self.search_input = self.container.get_by_placeholder("Search requirements...")
        self.create_new_requirement_button = self.container.get_by_role("button", name="Create New Requirement")
        self.cancel_button = self.container.get_by_role("button", name="Cancel")
        self.analyze_button = self.container.get_by_role("button", name="Analyze Requirement")

    def wait_for_loaded(self) -> Self:
        expect(self.container).to_be_visible()
        expect(self.title).to_have_text("Create Tests from Requirement")
        return self

    def search_requirement(self, query: str) -> Self:
        self.search_input.fill(query)
        return self

    def click_create_new_requirement(self) -> Self:
        self.create_new_requirement_button.click()
        return self

    def click_cancel(self) -> ProjectPage:
        self.cancel_button.click()
        return ProjectPage(self.page).wait_for_loaded()

    def click_analyze(self) -> Self:
        self.analyze_button.click()
        return self

    def close(self) -> ProjectPage:
        self.close_button.click()
        return ProjectPage(self.page).wait_for_loaded()


class TestOptionsDropdown:
    def __init__(self, page: Page):
        self.page = page
        self.container = page.locator("ul[data-ember-action]")
        self.folder_button = self.container.get_by_role("button").filter(has_text="Collection of suites")
        self.suite_button = self.container.get_by_role("button").filter(has_text="Collection of test cases")
        self.req_button = self.container.get_by_role("button").filter(has_text="Tests From Requirement")

    def wait_for_loaded(self) -> Self:
        expect(self.container).to_be_visible()
        # expect(self.folder_button).to_be_visible()
        return self

    def select_folder(self) -> CreateSuiteModal:
        self.folder_button.click()
        return CreateSuiteModal(self.page).wait_for_loaded(is_folder=True)

    def select_suite(self) -> CreateSuiteModal:
        self.suite_button.click()
        return CreateSuiteModal(self.page).wait_for_loaded(is_folder=False)

    def select_tests_from_requirement(self) -> CreateTestsFromRequirementModal:
        self.req_button.click()
        return CreateTestsFromRequirementModal(self.page).wait_for_loaded()


class ProjectPage:
    def __init__(self, page: Page):
        self.page = page
        self.side_bar = SideBar(page)

        self.breadcrumbs = page.locator(".breadcrumbs-page")
        self.project_title_link = self.breadcrumbs.locator("a.active")

        self.filter_button = page.locator(".filterbar-filter-btn-div button")
        self.search_input = page.get_by_placeholder("Search [Cmd + K]")
        self.tune_button = page.locator("button:has(.md-icon-tune)")

        self.test_button = page.get_by_role("button", name="Test", exact=True)
        self.test_options_button = page.locator(".btn-split-left")
        self.chat_with_tests_button = page.get_by_role("button", name="Chat with Tests")
        self.more_actions_button = page.locator(".ember-basic-dropdown-trigger").filter(
            has=page.locator(".md-icon-dots-horizontal")
        )

        self.manual_tab = page.get_by_role("link", name="Manual")
        self.automated_tab = page.get_by_role("link", name="Automated")
        self.out_of_sync_tab = page.get_by_role("link", name="Out of sync")
        self.detached_tab = page.get_by_role("link", name="Detached")
        self.starred_tab = page.get_by_role("link", name="Starred")

        self.display_button = page.get_by_role("button", name="Display")
        self.suites_list = page.locator(".suites-list-content")

    def wait_for_loaded(self) -> Self:
        expect(self.search_input).to_be_visible()
        expect(self.test_button).to_be_visible()
        return self

    def open_by_id(self, project_id: str) -> Self:
        self.page.goto(f"/projects/{project_id}")
        return self

    def verify_project_loaded(self, project_name: str) -> Self:
        expect(self.project_title_link).to_have_text(project_name)
        return self

    def search(self, text: str) -> Self:
        self.search_input.fill(text)
        return self

    def click_test_button(self) -> SelectSuiteModal:
        self.test_button.click()
        return SelectSuiteModal(self.page).wait_for_loaded()

    def open_test_options(self) -> TestOptionsDropdown:
        self.test_options_button.click()
        return TestOptionsDropdown(self.page).wait_for_loaded()

    def click_chat_with_tests(self) -> Self:
        self.chat_with_tests_button.click()
        return self

    def get_suite_locator(self, suite_name: str):
        return self.suites_list.locator(".dragSortItem").filter(has_text=suite_name)

    def open_suite(self, suite_name: str) -> Self:
        self.get_suite_locator(suite_name).get_by_role("link", name=suite_name).click()
        return self

    def edit_suite(self, suite_name: str) -> Self:
        suite = self.get_suite_locator(suite_name)
        suite.locator("button:has(.md-icon-pencil-box-outline)").click()
        return Self

    def delete_suite(self, suite_name: str) -> Self:
        suite = self.get_suite_locator(suite_name)
        suite.locator("button:has(.md-icon-trash-can-outline)").click()
        # Note: might need to handle a confirmation dialog here
        return self

    def verify_suite_present(self, suite_name: str) -> Self:
        expect(self.get_suite_locator(suite_name)).to_be_visible()
        return self
