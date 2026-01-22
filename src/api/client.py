import httpx

from src.api.models import LoginResponse, Project, ProjectAttributes, ProjectResponse


class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.client = httpx.Client(base_url=self.base_url, timeout=10.0)

    def login(self, api_token: str) -> str:
        url = "/api/login"
        payload = {"api_token": api_token}
        response = self.client.post(url, json=payload)
        response.raise_for_status()
        login_data = LoginResponse(**response.json())
        self.client.headers.update({"Authorization": login_data.jwt})
        return login_data.jwt

    def get_projects(self) -> ProjectResponse:
        url = "/api/projects"
        response = self.client.get(url)
        response.raise_for_status()
        data = response.json()

        projects = []
        for item in data.get("data", []):
            attributes = ProjectAttributes(
                title=item["attributes"].get("title"),
                description=item["attributes"].get("description"),
                kind=item["attributes"].get("kind"),
                framework=item["attributes"].get("framework"),
                language=item["attributes"].get("language"),
                created_at=item["attributes"].get("created-at"),
                updated_at=item["attributes"].get("updated-at"),
            )
            projects.append(
                Project(
                    id=item["id"], type=item["type"], attributes=attributes, relationships=item.get("relationships")
                )
            )

        return ProjectResponse(data=projects, meta=data.get("meta"), links=data.get("links"))
