from app.database.postgresql_snapshot_repository import save_snapshots
from app.models.repository_snapshot import RepositorySnapshot
from datetime import datetime

def test_postgresql_snapshot_save() -> None:
    date = datetime.now()
    test_snapshots = [RepositorySnapshot(65421,"test","test_repos",5441,date.isoformat()),
                      RepositorySnapshot(65421,"test","test_repos",5441,date.isoformat()),
                      RepositorySnapshot(564235,"test","test_repos_a",5441,date.isoformat()),
                      RepositorySnapshot(98542,"test","test_repos_b",5441,date.isoformat())
                      ]
    inserted_count,ignored_count = save_snapshots(test_snapshots)

    assert ignored_count == 1
    assert inserted_count == 3
    assert inserted_count + ignored_count == len(test_snapshots)