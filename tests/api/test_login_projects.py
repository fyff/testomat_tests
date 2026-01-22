from src.api.client import ApiClient


def test_login_and_get_projects(api_client: ApiClient):
    projects_response = api_client.get_projects()

    assert projects_response.data is not None
    assert len(projects_response.data) >= 0

    for project in projects_response.data:
        assert project.id is not None
        assert project.attributes.title is not None
        print(f"Project: {project.attributes.title} (ID: {project.id})")
