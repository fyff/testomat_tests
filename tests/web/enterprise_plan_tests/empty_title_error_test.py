import pytest
from faker import Faker

from src.web import Application


@pytest.mark.skip
@pytest.mark.web
def test_error_on_empty_suite_title(logged_app: Application):
    target_project_name = Faker().company()
    (logged_app.create_project_page.open().fill_project_title(target_project_name).click_create())
    details_page = logged_app.new_project_details_page.wait_for_loaded()
    details_page.close_readme()

    details_page.click_add_suite()
    details_page.verify_empty_title_error()

    details_page.click_add_folder()
    details_page.verify_empty_title_error()
