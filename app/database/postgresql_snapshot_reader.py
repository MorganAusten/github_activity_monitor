import psycopg
from app.models.repository_snapshot import RepositorySnapshot
from app.database.postgresql_client import get_postgresql_connection

def read_snapshots() -> list[RepositorySnapshot] :

    with get_postgresql_connection() as connection:

        print("connection PostgreSQL for read succeed")

        with  connection.cursor() as cursor:
            cursor.execute(""" SELECT repository_id, owner, name, stars, captured_at
              FROM snapshot_repository
              ORDER BY captured_at DESC, name ASC;
              """)
            rows = cursor.fetchall()

    result : list[RepositorySnapshot] = []

    for snapshot in rows:
        new_snapshot = RepositorySnapshot(snapshot[0],snapshot[1],
        snapshot[2],snapshot[3],snapshot[4].isoformat())
        result.append(new_snapshot)

    return result 

def read_snapshots_by_repository_id(repository_id : int) -> list[RepositorySnapshot]:
    with get_postgresql_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT repository_id, owner, name, stars, captured_at 
            FROM snapshot_repository 
            WHERE repository_id = %s
            ORDER BY captured_at DESC;
            """, (repository_id,))
            rows = cursor.fetchall()

    result : list[RepositorySnapshot] = []
    for row in rows:
        result.append(RepositorySnapshot(row[0],row[1],row[2],row[3],row[4].isoformat()))

    return result



if __name__ == "__main__":
    snapshots = read_snapshots_by_repository_id(20978623)
    print(len(snapshots))
    for snapshot in snapshots[:5]:
        print(snapshot)