from playwright.sync_api import Locator, Page, expect


class SuiteItem:
    """
    Represents a single row/folder/suite in the Project Details list.
    Root locator should be the specific .dragSortItem or .nestedItem div.
    """

    def __init__(self, page: Page, root_locator: Locator):
        self.page = page
        self.root = root_locator

        # Inner elements relative to the specific row
        self._title_link = self.root.locator("a.node-link")
        self._test_count = self.root.locator("a.node-link small")
        self._expand_btn = self.root.locator("button.expand")
        self._tags = self.root.locator("span.bg-gray-200")  # The badges like @for, @is

        # Toolbar actions (appear on hover/active)
        self._edit_btn = self.root.locator(".md-icon-pencil-box-outline")
        self._delete_btn = self.root.locator(".md-icon-trash-can-outline")

    def name(self) -> str:
        # The title text is inside the span, but we need to strip whitespace
        # and ensure we don't accidentally grab the 'small' text count
        return self._title_link.locator("span").first.text_content().strip()

    def get_test_count(self) -> str:
        # Returns string like "15 tests" or just "15" depending on your need
        return self._test_count.text_content().strip()

    def get_tags(self) -> list[str]:
        return self._tags.all_text_contents()

    def open(self):
        """Clicks the suite title to navigate inside."""
        self._title_link.click()

    def expand(self):
        """Expands the folder without navigating."""
        if self._expand_btn.is_visible():
            self._expand_btn.click()

    def click_edit(self):
        self._edit_btn.click()