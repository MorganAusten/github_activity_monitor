CREATE TABLE IF NOT EXISTS schema_migrations(
    migration_name TEXT NOT NULL,
    applied_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(migration_name)
)