from typing import Any
from app.models.repository import Repository


def map_repository_from_github(payload: dict[str, Any]) -> Repository:
    return Repository(
        id=payload["id"],
        owner=payload["owner"]["login"],
        name=payload["name"],
        html_url=payload["html_url"],
        language=payload.get("language"),
        stars=payload.get("stargazers_count", 0),
        created_at=payload["created_at"],
        updated_at=payload["updated_at"],
    )