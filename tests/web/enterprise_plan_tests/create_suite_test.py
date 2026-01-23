import pytest

from api.client import ApiClient
from web.application import Application


@pytest.mark.web
def test_create_suite_in_existing_project(api_client: ApiClient, logged_app: Application):
    pass


@pytest.mark.web
def test_create_suite_in_new_project(api_client: ApiClient, logged_app: Application):
    pass
