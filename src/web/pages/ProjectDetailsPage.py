from playwright.sync_api import Page, expect
from src.web.components.SuiteItem import SuiteItem


class ProjectDetailsPage:
    def __init__(self, page: Page):
        self.page = page

        # --- Header Locators ---
        # The active link in the breadcrumb tells us which project we are on
        self._active_project_link = page.locator(".breadcrumbs-page a.active")
        self._total_counter = page.locator(".new-counter.counter-btn-md")
        self._search_input = page.locator("input#search")

        # --- Action Buttons ---
        self._create_test_btn = page.locator("button", has_text="Test")  # The "Test +" button
        self._chat_ai_btn = page.locator("button.ai-btn")

        # --- Filter Tabs ---
        self._tab_manual = page.locator("a.filter-tab", has_text="Manual")
        self._tab_automated = page.locator("a.filter-tab", has_text="Automated")

        # --- List/Grid Locators ---
        # Locating the rows. The HTML uses a dragSortList structure.
        self._suite_items = page.locator(".dragSortList .dragSortItem")

    # --- Verification ---

    def is_loaded(self, project_name: str):
        """
        Verifies the page is loaded by checking the active breadcrumb title.
        """
        expect(self._active_project_link).to_be_visible()
        # Case insensitive check is safer
        expect(self._active_project_link).to_contain_text(project_name, ignore_case=True)

    def get_total_tests_count(self) -> int:
        """Returns the large number displayed next to the title (e.g. 26)."""
        text = self._total_counter.text_content().strip()
        return int(text) if text.isdigit() else 0

    # --- Actions ---

    def search(self, query: str):
        """Filters the suites/tests list."""
        self._search_input.fill(query)
        self.page.wait_for_load_state("networkidle")

    def click_manual_tab(self):
        self._tab_manual.click()

    def click_automated_tab(self):
        self._tab_automated.click()

    def click_create_test(self):
        self._create_test_btn.click()

    # --- Suite/Component Interaction ---

    def get_suite(self, suite_name: str) -> SuiteItem:
        """
        Finds a specific suite by name and returns the component.
        """
        # We filter the list of items to find the one containing the text
        target = self._suite_items.filter(has_text=suite_name).first
        return SuiteItem(self.page, target)

    def get_all_suites(self) -> list[SuiteItem]:
        """Returns all visible suites as objects."""
        count = self._suite_items.count()
        return [SuiteItem(self.page, self._suite_items.nth(i)) for i in range(count)]