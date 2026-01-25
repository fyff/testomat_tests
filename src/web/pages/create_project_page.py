from typing import Self

from playwright.sync_api import Page, expect

from src.web.pages.new_project_page import NewProjectPage


class CreateProjectPage:
    def __init__(self, page: Page):
        self.page = page
        self.form_container = page.locator("#content-desktop #new_project")
        self.how_to_start_link = page.get_by_role("link", name="How to start?")
        self.title = page.get_by_role("heading", name="New Project")
        self.project_title_input = page.locator("#project_title")

    def open(self) -> Self:
        self.page.goto("/projects/new")
        return self.wait_for_loaded()

    def wait_for_loaded(self) -> Self:
        expect(self.form_container).to_be_visible()
        expect(self.form_container.locator("#classical")).to_be_visible()
        expect(self.form_container.locator("#classical")).to_contain_text("Classical")
        expect(self.form_container.locator("#bdd")).to_be_visible()
        expect(self.form_container.locator("#bdd")).to_contain_text("BDD")
        expect(self.form_container.locator("#project_title")).to_be_visible()
        expect(self.form_container.locator("#demo-btn")).to_be_visible()
        expect(self.form_container.locator("#project-create-btn")).to_be_visible()
        expect(self.how_to_start_link).to_be_visible()
        expect(self.title).to_be_visible()
        return self

    def click_how_to_start(self) -> Self:
        self.how_to_start_link.click()
        return self

    def fill_project_title(self, project_name: str) -> Self:
        self.project_title_input.fill(project_name)
        return self

    def click_create(self) -> NewProjectPage:
        self.form_container.locator("#project-create-btn input").click()
        expect(self.form_container.locator("#project-create-btn input")).to_be_hidden(timeout=10_000)
        return NewProjectPage(self.page)
