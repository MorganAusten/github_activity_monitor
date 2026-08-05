import os
import psycopg
from app.models.repository_snapshot import RepositorySnapshot
from dotenv import load_dotenv

load_dotenv()

postgre_host = os.getenv("POSTGRES_HOST")
postgre_port = os.getenv("POSTGRES_PORT")
postgre_db = os.getenv("POSTGRES_DB")
postgre_user = os.getenv("POSTGRES_USER")
postgre_password = os.getenv("POSTGRES_PASSWORD")

def save_snapshots(repository_snapshots : list[RepositorySnapshot] ) -> tuple[int,int] :
    inserted_count = 0
    ignored_count = 0
    with psycopg.connect(host = postgre_host,
                    port= postgre_port,
                    dbname = postgre_db,
                    user =postgre_user,
                    password = postgre_password) as connection:

        print("Connection PostgreSQL succeed")

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