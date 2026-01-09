from playwright.sync_api import Page, expect


class SideBar:
    def __init__(self, page: Page):
        self.page = page

        self.container = page.locator('div.mainnav-menu')
        self.close_button = self.container.locator('button.btn-close')
        self.open_button = self.page.locator('button.btn-open')

        self.tests_link = self.container.get_by_role('link', name='Tests')
        self.requirements_link = self.container.get_by_role('link', name='Requirements')
        self.runs_link = self.container.get_by_role('link', name='Runs')
        self.plans_link = self.container.get_by_role('link', name='Plans')
        self.steps_link = self.container.get_by_role('link', name='Steps')
        self.pulse_link = self.container.get_by_role('link', name='Pulse')
        self.imports_link = self.container.get_by_role('link', name='Imports')
        self.analytics_link = self.container.get_by_role('link', name='Analytics')
        self.branches_link = self.container.get_by_role('link', name='Branches')
        self.settings_link = self.container.get_by_role('link', name='Settings')
        self.help_link = self.container.get_by_role('link', name='Help')
        self.projects_link = self.container.get_by_role('link', name='Projects')
        self.user_profile_link = self.container.get_by_role('link', name='Oleksii')

    def open(self) -> SideBar:
        self.container.hover()
        self.open_button.click()
        return self

    def close(self) -> SideBar:
        self.close_button.click()
        return self

    def is_loaded(self) -> SideBar:
        expect(self.container).to_be_visible()
        expect(self.tests_link).to_be_visible()
        expect(self.projects_link).to_be_visible()
        return self

    def navigate_to_tests(self) -> SideBar:
        self.tests_link.click()
        return self

    def navigate_to_requirements(self) -> SideBar:
        self.requirements_link.click()
        return self

    def navigate_to_runs(self) -> SideBar:
        self.runs_link.click()
        return self

    def navigate_to_plans(self) -> SideBar:
        self.plans_link.click()
        return self

    def navigate_to_steps(self) -> SideBar:
        self.steps_link.click()

    def navigate_to_pulse(self) -> SideBar:
        self.pulse_link.click()
        return self

    def navigate_to_imports(self) -> SideBar:
        self.imports_link.click()
        return self

    def navigate_to_analytics(self) -> SideBar:
        self.analytics_link.click()
        return self

    def navigate_to_branches(self) -> SideBar:
        self.branches_link.click()
        return self

    def navigate_to_settings(self) -> SideBar:
        self.settings_link.click()
        return self

    def navigate_to_help(self) -> SideBar:
        self.help_link.click()
        return self

    def navigate_to_projects(self) -> SideBar:
        self.projects_link.click()
        return self

    def navigate_to_user_profile(self) -> SideBar:
        self.user_profile_link.click()
        return self
