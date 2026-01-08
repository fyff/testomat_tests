from playwright.sync_api import Page

from src.web.pages.DashboardPage import DashboardPage
from src.web.pages.HomePage import HomePage
from src.web.pages.LoginPage import LoginPage
from src.web.pages.NewProjectPage import NewProjectPage
from src.web.pages.ProjectDeatilsPage import ProjectDeatilsPage


class Application:
    def __init__(self, page: Page):
        self.page = page
        self.home_page = HomePage(page)
        self.login_page = LoginPage(page)
        self.dashboard_page = DashboardPage(page)
        self.new_project_page = NewProjectPage(page)
        self.project_details_page = ProjectDeatilsPage(page)
