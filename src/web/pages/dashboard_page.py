from typing import Self

from playwright.sync_api import Locator, Page, expect

from src.web.components.auth_header import AuthHeader
from src.web.components.project_card import ProjectCard
from src.web.components.side_bar import SideBar
from src.web.pages.new_project_page import NewProjectPage


class DashboardPage:
    def __init__(self, page: Page):
        self.page = page
        self.side_bar = SideBar(page)
        self.auth_header = AuthHeader(page)

        self.header_title = page.locator("h2", has_text="Projects")
        self.company_dropdown = page.locator("#company_id")
        self.search_input = page.locator("#content-desktop #search")
        self.create_button = page.get_by_role("link", name="Create", exact=True)
        self.flash_message = page.locator(".common-flash-success-right")
        self.plan_tooltip = page.locator(".tooltip-project-plan")
        self.grid_view_button = page.locator("#grid-view")
        self.grid_items = page.locator("#grid li")
        self.table_view_button = page.locator("#table-view")
        self.table_rows = page.locator("#myTable tbody tr")
        self.create_company_link = page.get_by_role("link", name="Create Company to Upgrade")
        self.empty_state_message = page.get_by_text("You have not created any projects yet")
        self.empty_state_create_project_button = page.get_by_role("link", name="Create project")
        self.docs_link = page.get_by_role("link", name="Read docs →")
        self.chat_button = page.locator("#crisp-chatbox").get_by_role("button")
        self.chat_opened_indicator = page.locator("#crisp-chatbox [data-id='chat_opened']")
        self.jest_tutorial_title = page.get_by_role("heading", name="🚀 Learn How To Start with Jest Tests")
        self.cucumber_tutorial_title = page.get_by_role("heading", name="🤓 Get Started with Cucumber BDD Tests")
        self.cypress_tutorial_title = page.get_by_role("heading", name="🌲 Integrate Cypress.io Tests")
        self.no_project_image = page.locator('img[src="/images/projects/no-project.svg"]')

    def open(self, url: str = "/projects") -> Self:
        self.page.goto(url)
        return self.wait_for_loaded()

    def wait_for_loaded(self) -> Self:
        self.auth_header.wait_for_loaded()
        expect(self.header_title).to_be_visible()
        expect(self.company_dropdown).to_be_visible()
        expect(self.create_button).to_be_visible()
        expect(self.grid_view_button).to_be_visible()
        expect(self.table_view_button).to_be_visible()
        expect(self.chat_button).to_be_visible()
        return self

    def verify_educational_videos(self):
        expect(self.jest_tutorial_title).to_be_visible()
        expect(self.cucumber_tutorial_title).to_be_visible()
        expect(self.cypress_tutorial_title).to_be_visible()

    def click_create_company(self):
        self.create_company_link.click()

    def click_read_docs(self):
        self.docs_link.click()

    def select_company(self, company_label: str):
        self.company_dropdown.select_option(label=company_label)

    def search_project(self, target_project: str) -> Self:
        expect(self.page.get_by_role("searchbox", name="Search")).to_be_visible()
        self.page.locator("#content-desktop #search").fill(target_project)
        return self

    def create_project(self) -> NewProjectPage:
        self.create_button.click()
        return NewProjectPage(self.page).wait_for_loaded()

    def switch_to_table_view(self) -> Self:
        self.table_view_button.click()
        expect(self.page.locator("#myTable")).to_be_visible()
        return self

    @property
    def get_table_rows_locator(self):
        return self.table_rows

    def switch_to_grid_view(self) -> Self:
        self.grid_view_button.click()
        expect(self.grid_items.first).to_be_visible()
        return self

    @property
    def get_project_card_locator(self):
        return self.grid_items

    @property
    def get_plan_badge(self) -> Locator:
        return self.plan_tooltip

    def get_project(self, project_name: str) -> ProjectCard:
        card_locator = self.grid_items.filter(has=self.page.locator("h3", has_text=project_name)).first
        return ProjectCard(card_locator)

    def get_all_projects(self) -> list[ProjectCard]:
        expect(self.grid_items.first).to_be_visible()
        return [ProjectCard(item) for item in self.grid_items.all()]
