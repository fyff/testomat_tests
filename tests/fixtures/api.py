import pytest

from src.api.client import ApiClient
from tests.fixtures.config import Config


@pytest.fixture(scope="session")
def api_client(configs: Config) -> ApiClient:
    client = ApiClient(configs.app_base_url)
    client.login(configs.testomat_general_token)
    return client
