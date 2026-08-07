from pathlib import Path
from app.database.postgresql_client import get_postgresql_connection

def run_migrations() -> None:
    path = Path("sql")
    files = sorted(path.glob("*.sql"))

    if not files :
        raise ValueError("No migrations in sql directory")
    if files[0].name != "000_create_schema_migrations_table.sql":
        raise ValueError("bootstrap file is wrong.")
    
    with get_postgresql_connection() as connection:
        with connection.cursor() as cursor:
            bootstrap_sql = files[0].read_text(encoding="utf-8")
            cursor.execute(bootstrap_sql)

            cursor.execute("""SELECT migration_name
FROM schema_migrations;""")
            rows = cursor.fetchall()

            migration_name_set = { row[0] for row in rows}
            for file in files[1:]:
                if file.name not in migration_name_set:
                    print(file.name)
                    cursor.execute(file.read_text(encoding="utf-8"))
                    cursor.execute("""
                    INSERT INTO schema_migrations(migration_name)
                    VALUES (%s)
                    """, (file.name,))
                    
if __name__ == "__main__":
    run_migrations()
    