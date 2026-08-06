import os
import psycopg
from dotenv import load_dotenv
from app.models.repository_snapshot import RepositorySnapshot

load_dotenv()

postgre_host = os.getenv("POSTGRES_HOST")
postgre_port = os.getenv("POSTGRES_PORT")
postgre_db = os.getenv("POSTGRES_DB")
postgre_user = os.getenv("POSTGRES_USER")
postgre_password = os.getenv("POSTGRES_PASSWORD")

def read_snapshots() -> list[RepositorySnapshot] :

    with psycopg.connect(host = postgre_host,
                    port= postgre_port,
                    dbname = postgre_db,
                    user =postgre_user,
                    password = postgre_password) as connection:

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
    with psycopg.connect(host = postgre_host,
                    port= postgre_port,
                    dbname = postgre_db,
                    user =postgre_user,
                    password = postgre_password) as connection:
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