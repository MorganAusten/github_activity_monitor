CREATE TABLE IF NOT EXISTS snapshot_repository (
    repository_id BIGINT NOT NULL,
    owner TEXT NOT NULL,
    name TEXT NOT NULL,
    stars INTEGER NOT NULL,
    captured_at TIMESTAMP NOT NULL,
    UNIQUE(repository_id,captured_at) 
)