from playwright.sync_api import Locator, Page, expect


class ProjectCard:
    def __init__(self, page: Page, root_locator: Locator):
        self.page = page
        self.root = root_locator

        self._title = self.root.locator("h3")
        self._link = self.root.locator("a").first
        self._stats = self.root.locator("p.text-gray-500")
        self._badges = self.root.locator(".project-badges .common-badge")
        # Locates only the image tags inside the user section
        self._avatar_imgs = self.root.locator(".inline-flex img")
        # Locates the "+N members" overflow circle if it exists
        self._avatar_overflow = self.root.locator(".inline-flex div.rounded-full")

    def open(self):
        self._link.click()

    def has_title(self, title: str):
        expect(self._title).to_have_text(title)

    def has_test_count(self, count: str):
        expect(self._stats).to_contain_text(count)

    def has_badge(self, badge_name: str):
        expect(self._badges.filter(has_text=badge_name)).to_be_visible()

    def is_demo_project(self):
        demo_badge = self._badges.filter(has_text="Demo")
        #TODO consultation required. There was regexp.(re.compile(r"class"))
        expect(demo_badge).to_be_visible()
        expect(demo_badge).to_have_class("common-badge common-badge-project-demo")

    def has_team_members_count(self, count: int):
        """
        Checks the number of visible avatar images.
        Note: This does not include the '+N' number, only actual images.
        """
        expect(self._avatar_imgs).to_have_count(count)

    def has_team_overflow(self):
        """Checks if the +N (e.g., +32) bubble is visible."""
        expect(self._avatar_overflow).to_be_visible()
