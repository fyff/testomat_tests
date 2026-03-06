import pytest
from faker import Faker

from src.api import ApiClient
from src.web import Application


@pytest.mark.regression
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
        .close_detail_view()
    )

    logged_app.project_page.verify_suite_present(suite_name)


@pytest.mark.regression
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
        .close_detail_view()
    )

    logged_app.project_page.verify_suite_present(folder_name)


@pytest.mark.order(2)
@pytest.mark.smoke
def test_delete_project(api_client: ApiClient, logged_app: Application):
    projects = api_client.get_projects().data
    sorted_projects = sorted(projects, key=lambda x: x.attributes.created_at, reverse=True)
    target_project = sorted_projects[0]
    target_project_id = target_project.id
    target_project_name = target_project.attributes.title

    logged_app.project_page.open_by_id(target_project_id).wait_for_loaded()

    (logged_app.side_bar.open().navigate_to_settings().click_administration().delete_project().verify_deletion_toast())

    logged_app.page.goto("/projects")
    logged_app.dashboard_page.search_project(target_project_name)
    logged_app.dashboard_page.verify_project_absent(target_project_name)

    response = api_client.get_project(target_project_id)
    assert response.status_code == 404
