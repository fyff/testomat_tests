import pytest
from faker import Faker

from src.web.Application import Application
from tests.conftest import Config

faker = Faker()


invalid_login_test_cases = [
    # ECP: Invalid Credentials
    pytest.param("config_email", faker.password(), id="valid_email_invalid_password"),
    pytest.param(faker.email(), "config_password", id="invalid_email_valid_password"),
    pytest.param(faker.email(), faker.password(), id="invalid_email_invalid_password"),

    # BVA: Empty Fields
    pytest.param("config_email", "", id="valid_email_empty_password"),
    pytest.param("", "config_password", id="empty_email_valid_password"),
    pytest.param("", "", id="empty_email_empty_password"),

    # BVA: Malformed Email
    pytest.param("malformed_email_no_at_sign", "config_password", id="malformed_email_no_at"),
    pytest.param("user@domain", "config_password", id="malformed_email_no_tld"),
    pytest.param("user@.com", "config_password", id="malformed_email_no_domain_name"),
    pytest.param("malformed@email", faker.password(), id="malformed_email_general"),

    # BVA: Min/Max Length (Email)
    pytest.param("a@b", "config_password", id="email_too_short"),
    pytest.param("a@b.c", "config_password", id="email_min_length_valid"),  # 5 chars
    pytest.param(faker.pystr(min_chars=240, max_chars=240) + "@example.com", "config_password",
                 id="email_max_length_valid"),  # approx 252 chars
    pytest.param(faker.pystr(min_chars=250, max_chars=250) + "@example.com", "config_password",
                 id="email_over_max_length"),  # approx 262 chars

    # BVA: Min/Max Length (Password)
    pytest.param("1234567", "config_email", id="password_too_short"),  # 7 chars, assuming min 8
    pytest.param("12345678", "config_email", id="password_min_length_valid"),  # 8 chars
    pytest.param(faker.pystr(min_chars=128, max_chars=128), "config_email",
                 id="password_max_length_valid"),  # 128 chars
    pytest.param(faker.pystr(min_chars=129, max_chars=129), "config_email",
                 id="password_over_max_length"),  # 129 chars

    # Security: XSS
    pytest.param(faker.email() + "<script>alert('xss')</script>", "config_password", id="xss_email"),
    pytest.param("config_email", "password<script>alert('xss')</script>", id="xss_password"),

    # Security: SQL Injection
    pytest.param("admin' OR '1'='1", "config_password", id="sql_injection_email_or"),
    pytest.param("admin' --", "config_password", id="sql_injection_email_comment"),
    pytest.param("config_email", "password' OR '1'='1", id="sql_injection_password_or"),
    pytest.param("config_email", "password' --", id="sql_injection_password_comment"),
]


@pytest.mark.parametrize("email, password", invalid_login_test_cases)
def test_login_invalid_ecp_bva(shared_page: Application, configs: Config, email: str, password: str):
    if email == "config_email":
        email = configs.email
    if password == "config_password":
        password = configs.password

    shared_page.login_page.open()
    shared_page.login_page.is_loaded()
    shared_page.login_page.login(email, password)
    shared_page.login_page.invalid_login_message_visible()

    shared_page.page.wait_for_timeout(2000)

def test_login_with_valid_creds(app: Application, configs: Config):
    home_page = app.home_page
    home_page.open()
    home_page.is_loaded()
    home_page.click_login()

    login_page = app.login_page
    login_page.is_loaded()
    login_page.login(configs.email, configs.password)
    app.dashboard_page.is_loaded()
