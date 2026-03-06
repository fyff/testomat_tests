from dataclasses import dataclass
from typing import Any, Self


@dataclass
class ProjectAttributes:
    title: str
    description: str | None = None
    kind: str | None = None
    framework: str | None = None
    language: str | None = None
    created_at: str | None = None
    updated_at: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            title=data["title"],
            description=data.get("description"),
            kind=data.get("kind"),
            framework=data.get("framework"),
            language=data.get("language"),
            created_at=data.get("created-at"),
            updated_at=data.get("updated-at"),
        )


@dataclass
class Project:
    id: str
    type: str
    attributes: ProjectAttributes
    relationships: dict[str, Any] | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            id=data["id"],
            type=data["type"],
            attributes=ProjectAttributes.from_dict(data["attributes"]),
            relationships=data.get("relationships"),
        )


@dataclass
class ProjectResponse:
    data: list[Project]
    meta: dict[str, Any] | None = None
    links: dict[str, Any] | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            data=[Project.from_dict(item) for item in data.get("data", [])],
            meta=data.get("meta"),
            links=data.get("links"),
        )


@dataclass
class LoginResponse:
    jwt: str
