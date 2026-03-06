from __future__ import annotations

from typing import TYPE_CHECKING, Self

from playwright.sync_api import Page, expect

if TYPE_CHECKING:
    from ..pages import DashboardPage, ProjectSettingsPage


class SideBar:
    def __init__(self, page: Page):
        self.page = page

        self.container = page.locator("div.mainnav-menu")
        self.close_button = self.container.locator("button.btn-close")
        self.open_button = self.page.locator("button.btn-open")

        self.tests_link = self.container.get_by_role("link", name="Tests")
        self.requirements_link = self.container.get_by_role("link", name="Requirements")
        self.runs_link = self.container.get_by_role("link", name="Runs")
        self.plans_link = self.container.get_by_role("link", name="Plans")
        self.steps_link = self.container.get_by_role("link", name="Steps")
        self.pulse_link = self.container.get_by_role("link", name="Pulse")
        self.imports_link = self.container.get_by_role("link", name="Imports")
        self.analytics_link = self.container.get_by_role("link", name="Analytics")
        self.branches_link = self.container.get_by_role("link", name="Branches")
        self.settings_link = self.container.get_by_role("link", name="Settings")
        self.help_link = self.container.get_by_role("link", name="Help")
        self.projects_link = self.container.get_by_role("link", name="Projects")
        self.user_profile_link = self.container.get_by_role("link", name="Oleksii")

    def open(self) -> Self:
        self.container.hover()
        self.open_button.click()
        return self

    def close(self) -> Self:
        self.close_button.click()
        return self

    def wait_for_loaded(self) -> Self:
        expect(self.container).to_be_visible()
        expect(self.tests_link).to_be_visible()
        expect(self.projects_link).to_be_visible()
        return self

    def navigate_to_tests(self) -> Self:
        self.tests_link.click()
        return self

    def navigate_to_requirements(self) -> Self:
        self.requirements_link.click()
        return self

    def navigate_to_runs(self) -> Self:
        self.runs_link.click()
        return self

    def navigate_to_plans(self) -> Self:
        self.plans_link.click()
        return self

    def navigate_to_steps(self) -> Self:
        self.steps_link.click()
        return self

    def navigate_to_pulse(self) -> Self:
        self.pulse_link.click()
        return self

    def navigate_to_imports(self) -> Self:
        self.imports_link.click()
        return self

    def navigate_to_analytics(self) -> Self:
        self.analytics_link.click()
        return self

    def navigate_to_branches(self) -> Self:
        self.branches_link.click()
        return self

    def navigate_to_settings(self) -> ProjectSettingsPage:
        from ..pages import ProjectSettingsPage

        self.settings_link.click()
        return ProjectSettingsPage(self.page).wait_for_loaded()

    def navigate_to_help(self) -> Self:
        self.help_link.click()
        return self

    def navigate_to_projects(self) -> DashboardPage:
        from ..pages import DashboardPage

        self.page.goto("/projects")
        return DashboardPage(self.page).wait_for_loaded()

    def navigate_to_user_profile(self) -> Self:
        self.user_profile_link.click()
        return self
