from app.models.repository import Repository
from datetime import datetime
from dataclasses import dataclass

@dataclass

class RepositorySnapshot:
    repository_id : int
    owner : str
    name : str
    language : str | None
    stars : int
    captured_at : str

def make_repository_snapshot(repository : Repository, captured_at : datetime) -> RepositorySnapshot:
    return RepositorySnapshot(
        repository_id=repository.id,
        owner=repository.owner,
        name=repository.name,
        language= repository.language,
        stars=repository.stars,
        captured_at= captured_at.isoformat()
    )
