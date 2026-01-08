from typing import Self

from playwright.sync_api import expect, Page


class NewProjectPage:
    def __init__(self, page: Page):
        self.page = page
        self.__form_container = page.locator("#content-desktop #new_project")
        self._how_to_start_link = page.get_by_role("link", name="How to start?")
        self._title = page.get_by_role("heading", name="New Project")
        self._project_title_input = page.locator("#project_title")

    def open(self) -> Self:
        self.page.goto("/projects/new")
        return self

    def is_loaded(self) -> Self:
        expect(self.__form_container).to_be_visible()
        expect(self.__form_container.locator("#classical")).to_be_visible()
        expect(self.__form_container.locator("#classical")).to_contain_text("Classical")
        expect(self.__form_container.locator("#bdd")).to_be_visible()
        expect(self.__form_container.locator("#bdd")).to_contain_text("BDD")
        expect(self.__form_container.locator("#project_title")).to_be_visible()
        expect(self.__form_container.locator("#demo-btn")).to_be_visible()
        expect(self.__form_container.locator("#project-create-btn")).to_be_visible()
        expect(self._how_to_start_link).to_be_visible()
        expect(self._title).to_be_visible()
        return self

    def click_how_to_start(self) -> Self:
        self._how_to_start_link.click()
        return self

    def fill_project_title(self, project_name: str) -> Self:
        self._project_title_input.fill(project_name)
        return self

    def click_create(self) -> Self:
        self.__form_container.locator("#project-create-btn input").click()
        expect(self.__form_container.locator("#project-create-btn input")).to_be_hidden(timeout=10_000)
        return self
