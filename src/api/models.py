from dataclasses import dataclass
from typing import Any


@dataclass
class ProjectAttributes:
    title: str
    description: str | None = None
    kind: str | None = None
    framework: str | None = None
    language: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    # Add other attributes as needed based on actual API response


@dataclass
class Project:
    id: str
    type: str
    attributes: ProjectAttributes
    relationships: dict[str, Any] | None = None


@dataclass
class ProjectResponse:
    data: list[Project]
    meta: dict[str, Any] | None = None
    links: dict[str, Any] | None = None


@dataclass
class LoginResponse:
    jwt: str
