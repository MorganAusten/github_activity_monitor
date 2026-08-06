from app.database.postgresql_snapshot_repository import save_snapshots , delete_postgresql_snapshots_by_repository
from app.models.repository_snapshot import RepositorySnapshot
from datetime import datetime

def test_postgresql_snapshot_save() -> None:

    date = datetime.now()
    base_repository = int(date.timestamp()) * 1_000_000

    repositories_ids = [
        base_repository,
        base_repository +1,
        base_repository +2
    ]

    test_snapshots = [RepositorySnapshot(repository_id= repositories_ids[0],owner = "test",name= "test_repos",
                    language = "C++", stars = 5441,captured_at = date.isoformat()),

                      RepositorySnapshot(repository_id= repositories_ids[0],owner = "test",name= "test_repos",
                      language = "C++", stars = 5441,captured_at = date.isoformat()),

                      RepositorySnapshot(repository_id= repositories_ids[1], owner = "test",name= "test_repos_a",
                      language = "C++", stars = 5441,captured_at = date.isoformat()),

                      RepositorySnapshot(repository_id= repositories_ids[2],owner = "test",name= "test_repos_b",
                      language = "C++", stars = 5441,captured_at = date.isoformat())
                      ]
    try:
        inserted_count,ignored_count = save_snapshots(test_snapshots)

        assert ignored_count == 1
        assert inserted_count == 3
        assert inserted_count + ignored_count == len(test_snapshots)
    finally:
        for repository_id in repositories_ids : delete_postgresql_snapshots_by_repository(repository_id)
