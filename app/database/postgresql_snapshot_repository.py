from app.models.repository_snapshot import RepositorySnapshot
from app.database.postgresql_client import get_postgresql_connection

def save_snapshots(repository_snapshots : list[RepositorySnapshot] ) -> tuple[int,int] :

    inserted_count = 0
    ignored_count = 0

    with get_postgresql_connection() as connection:

        print("connection PostgreSQL for save succeed")

        with  connection.cursor() as cursor:
            for repository_snapshot in repository_snapshots:
                cursor.execute(  """
                INSERT INTO snapshot_repository (
                    repository_id,
                    owner,
                    name,
                    stars,
                    captured_at
                )
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (repository_id,captured_at) DO NOTHING;
                """,(
                    repository_snapshot.repository_id,
                    repository_snapshot.owner,
                    repository_snapshot.name,
                    repository_snapshot.stars,
                    repository_snapshot.captured_at
                ))

                if cursor.rowcount == 1 :
                    inserted_count += 1
                else:
                    ignored_count += 1

    return (inserted_count,ignored_count)

def delete_postgresql_snapshots_by_repository(repository_id : int) -> int:

    with get_postgresql_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
            DELETE FROM snapshot_repository
            WHERE repository_id = %s;
            """,
            (repository_id,))
            delete_count = cursor.rowcount

    return delete_count