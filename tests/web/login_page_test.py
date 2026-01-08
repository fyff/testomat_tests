from faker import Faker

from src.web.Application import Application
from tests.conftest import Config


def test_login_invalid(app: Application, configs: Config):
    home_page = app.home_page
    home_page.open()
    home_page.is_loaded()
    home_page.click_login()

    login_page = app.login_page
    login_page.is_loaded()
    login_page.login(configs.email, Faker().password(length=10))
    login_page.invalid_login_message_visible()


def test_login_with_valid_creds(app: Application, configs: Config):
    home_page = app.home_page
    home_page.open()
    home_page.is_loaded()
    home_page.click_login()

    login_page = app.login_page
    login_page.is_loaded()
    login_page.login(configs.email, configs.password)
    app.dashboard_page.is_loaded()
