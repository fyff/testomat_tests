from playwright.sync_api import Page

from src.web.pages.dashboard_page import DashboardPage
from src.web.pages.home_page import HomePage
from src.web.pages.login_page import LoginPage
from src.web.pages.new_project_page import NewProjectPage
from src.web.pages.project_details_page import ProjectDeatilsPage


class Application:
    def __init__(self, page: Page):
        self.page = page
        self.home_page = HomePage(page)
        self.login_page = LoginPage(page)
        self.dashboard_page = DashboardPage(page)
        self.new_project_page = NewProjectPage(page)
        self.project_details_page = ProjectDeatilsPage(page)
