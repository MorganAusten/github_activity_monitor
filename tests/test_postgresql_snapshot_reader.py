from app.database.postgresql_snapshot_repository import save_snapshots , delete_postgresql_snapshots_by_repository
from app.database.postgresql_snapshot_reader import read_snapshots_by_repository_id
from datetime import datetime,timedelta
from app.models.repository_snapshot import RepositorySnapshot


def test_postgresql_snapshot_reader():

    older_date = datetime.now()
    newer_date = older_date + timedelta(seconds= 1)

    test_repository_id = int(older_date.timestamp() * 1_000_000)
    print(f"test repository id : {test_repository_id}")

    snapshots : list[RepositorySnapshot] = [
        RepositorySnapshot(test_repository_id,"owner","name",475,older_date.isoformat()),
        RepositorySnapshot(test_repository_id,"owner","name",476,newer_date.isoformat())
    ]
    try:
        save_snapshots(snapshots)
        results = read_snapshots_by_repository_id(test_repository_id)

        assert len(results) == 2
        for result in results:
            assert result.repository_id == test_repository_id
        assert results[0].captured_at == newer_date.isoformat()
        assert results[1].captured_at == older_date.isoformat()
    finally:
        deleted_count = delete_postgresql_snapshots_by_repository(test_repository_id)

    print(f"deleted test snapshots {deleted_count}")
