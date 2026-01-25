import pytest
from faker import Faker

from src.api.client import ApiClient
from src.web.application import Application


@pytest.mark.web
def test_create_suite_in_existing_project(api_client: ApiClient, logged_app: Application):
    projects = api_client.get_projects()
    target_project_id = projects.data[0].id

    logged_app.project_page.open_by_id(target_project_id).wait_for_loaded()

    suite_name = Faker().company()
    (
        logged_app.project_page.open_test_options()
        .select_suite()
        .wait_for_loaded(is_folder=False)
        .fill_title(suite_name)
        .click_save()
    )

    logged_app.project_page.verify_suite_present(suite_name)


def test_create_folder_in_existing_project(api_client: ApiClient, logged_app: Application):
    projects = api_client.get_projects()
    target_project_id = projects.data[0].id

    logged_app.project_page.open_by_id(target_project_id).wait_for_loaded()

    folder_name = Faker().company()
    (
        logged_app.project_page.open_test_options()
        .select_folder()
        .wait_for_loaded(is_folder=True)
        .fill_title(folder_name)
        .click_save()
    )

    logged_app.project_page.verify_suite_present(folder_name)
