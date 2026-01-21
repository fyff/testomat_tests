from playwright.sync_api import Page

from src.web.components.crisp_chat import CrispChat
from src.web.pages.dashboard_page import DashboardPage
from src.web.pages.landing_page import LandingPage
from src.web.pages.login_page import LoginPage
from src.web.pages.new_project_details_page import NewProjectDetailsPage
from src.web.pages.new_project_page import NewProjectPage


class Application:
    def __init__(self, page: Page):
        self.page = page
        self.home_page = LandingPage(page)
        self.login_page = LoginPage(page)
        self.dashboard_page = DashboardPage(page)
        self.new_project_page = NewProjectPage(page)
        self.new_project_details_page = NewProjectDetailsPage(page)
        self.crisp_chat = CrispChat(page)
