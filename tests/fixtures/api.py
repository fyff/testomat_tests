from collections.abc import Generator

import pytest

from src.api.client import ApiClient
from tests.fixtures.config import Config


@pytest.fixture(scope="session")
def api_client(configs: Config) -> Generator[ApiClient]:
    client = ApiClient(base_url=configs.app_base_url, api_token=configs.testomat_general_token)
    yield client
    client.close()
