import pytest
from selenium import webdriver


@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(0)
    driver.set_window_size(1680, 1050)
    yield driver
    driver.quit()
