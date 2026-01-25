from collections.abc import Generator
from typing import Self

import httpx

from src.api.models import ProjectResponse


class TestomatAuth(httpx.Auth):
    def __init__(self, base_url: str, api_token: str):
        self.base_url = base_url.rstrip("/")
        self.api_token = api_token
        self.jwt: str | None = None

    def auth_flow(self, request: httpx.Request) -> Generator[httpx.Request, httpx.Response]:
        if self.jwt is None:
            self._fetch_jwt()

        request.headers["Authorization"] = self.jwt
        yield request

    def _fetch_jwt(self):
        # We use a separate context-less client to avoid infinite recursion
        # or side effects from the main client settings.
        with httpx.Client(base_url=self.base_url) as client:
            response = client.post("/api/login", json={"api_token": self.api_token})
            response.raise_for_status()
            self.jwt = response.json().get("jwt")


class ApiClient:
    def __init__(self, base_url: str, api_token: str):
        self.base_url = base_url.rstrip("/")
        self.client = httpx.Client(base_url=self.base_url, timeout=10.0, auth=TestomatAuth(base_url, api_token))

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.client.close()

    def get_projects(self) -> ProjectResponse:
        url = "/api/projects"
        response = self.client.get(url)
        response.raise_for_status()
        return ProjectResponse.from_dict(response.json())
