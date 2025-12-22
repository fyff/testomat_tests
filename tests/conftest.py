import os

import pytest
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="session")
def configs():
    return {
        "base_url": f"{os.getenv("BASE_URL")}",
        "login_url": f"{os.getenv("BASE_APP_URL")}/users/sign_in",
        "email": os.getenv("EMAIL"),
        "password": os.getenv("PASSWORD"),
    }
