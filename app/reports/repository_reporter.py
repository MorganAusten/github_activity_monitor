from app.models.repository import Repository
from dataclasses import dataclass

@dataclass

class RepositoryReport:
    total_repositories: int
    repositories_by_language: dict[str, int]
    average_stars: float
    most_starred_repository: Repository | None

def build_repository_report(repositories: list[Repository]) -> RepositoryReport:

    total_repositories = len(repositories)
    repositories_by_language : dict[str, int] = {}
    most_starred_repository: Repository | None = None
    total_stars = 0
    
    for repository in repositories:
        total_stars += repository.stars
        language = repository.language or "Unknown"
        repositories_by_language[language] = (repositories_by_language.get(language,0) + 1)
        if most_starred_repository is None: 
            most_starred_repository = repository
        elif most_starred_repository.stars < repository.stars:
            most_starred_repository = repository
    
    average_stars = total_stars/total_repositories 
    
    return RepositoryReport(total_repositories,repositories_by_language,average_stars,most_starred_repository)





