from playwright.sync_api import Page, expect, Locator

from src.web.components.ProjectCard import ProjectCard
from src.web.components.SideBar import SideBar


class DashboardPage:
    def __init__(self, page: Page):
        self.page = page
        self.side_bar = SideBar(page)

        self._header_title = page.locator("h2", has_text="Projects")
        self._company_dropdown = page.locator("#company_id")
        self._search_input = page.locator("#content-desktop #search")
        self._create_button = page.locator("a.common-btn-primary", has_text="Create")
        self._flash_message = page.locator(".common-flash-success-right")
        self._plan_tooltip = page.locator(".tooltip-project-plan")
        self._grid_view_button = page.locator("#grid-view")
        self._grid_items = page.locator("#grid li")
        self._table_view_button = page.locator("#table-view")
        self._table_rows = page.locator("#myTable tbody tr")

    def is_loaded(self):
        expect(self._header_title).to_be_visible()
        expect(self.page.locator(".common-flash-success-right")).to_be_visible()
        expect(self.page.locator(".common-flash-success-right")).to_have_text("Signed in successfully")
        expect(self.page.locator(".common-flash-success-right", has_text="Signed in successfully")).to_be_visible()

    def search_project(self, target_project: str):
        expect(self.page.get_by_role("searchbox", name="Search")).to_be_visible()
        self.page.locator("#content-desktop #search").fill(target_project)

    def select_company(self, company_label: str):
        self._company_dropdown.select_option(label=company_label)

    def create_project(self):
        self._create_button.click()

    def switch_to_table_view(self):
        self._table_view_button.click()
        expect(self.page.locator("#myTable")).to_be_visible()

    @property
    def get_table_rows_locator(self):
        return self._table_rows

    def switch_to_grid_view(self):
        self._grid_view_button.click()
        expect(self._grid_items.first).to_be_visible()

    @property
    def get_project_card_locator(self):
        return self._grid_items

    @property
    def get_plan_badge(self) -> Locator:
        return self._plan_tooltip

    def get_project(self, project_name: str) -> ProjectCard:
        card_locator = self._grid_items.filter(has=self.page.locator("h3", has_text=project_name)).first
        return ProjectCard(self.page, card_locator)

    def get_all_projects(self) -> list[ProjectCard]:
        expect(self._grid_items.first).to_be_visible()
        return [ProjectCard(self.page, item) for item in self._grid_items.all()]
