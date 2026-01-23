from playwright.sync_api import Page

from src.web.components.auth_header import AuthHeader
from src.web.components.crisp_chat import CrispChat
from src.web.components.side_bar import SideBar
from src.web.pages.create_project_page import CreateProjectPage
from src.web.pages.dashboard_page import DashboardPage
from src.web.pages.landing_page import LandingPage
from src.web.pages.login_page import LoginPage
from src.web.pages.new_project_details_page import NewProjectDetailsPage


class Application:
    def __init__(self, page: Page):
        self.page = page
        self.landing_page = LandingPage(page)
        self.login_page = LoginPage(page)
        self.dashboard_page = DashboardPage(page)
        self.create_project_page = CreateProjectPage(page)
        self.new_project_details_page = NewProjectDetailsPage(page)

        # global components
        self.crisp_chat = CrispChat(page)
        self.auth_header = AuthHeader(page)
        self.side_bar = SideBar(page)
