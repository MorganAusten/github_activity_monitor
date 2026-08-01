from app.models.repository import Repository 

def repository_filter(repositories: list[Repository], language: str | None = None, stars: int | None = None) -> list[Repository]:

    if not language and not stars:
        raise ValueError("At least one filter must be provided")

    return [repository
    for repository in repositories
        if (language is None or repository.language == language) and (stars is None or repository.stars >= stars)
    ]