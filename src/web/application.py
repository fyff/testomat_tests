from playwright.sync_api import Page

from src.web.components import AuthHeader, CrispChat, SideBar
from src.web.pages import (
    CreateProjectPage,
    DashboardPage,
    LandingPage,
    LoginPage,
    NewProjectPage,
    ProjectPage,
    ProjectSettingsPage,
)


class Application:
    def __init__(self, page: Page):
        self.page = page
        self.landing_page = LandingPage(page)
        self.login_page = LoginPage(page)
        self.dashboard_page = DashboardPage(page)
        self.create_project_page = CreateProjectPage(page)
        self.new_project_details_page = NewProjectPage(page)
        self.project_page = ProjectPage(page)
        self.project_settings_page = ProjectSettingsPage(page)

        # global components
        self.crisp_chat = CrispChat(page)
        self.auth_header = AuthHeader(page)
        self.side_bar = SideBar(page)
