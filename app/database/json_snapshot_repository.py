from dataclasses import asdict
from pathlib import Path
import json
from app.models.repository_snapshot import RepositorySnapshot

def save_snapshots_as_json(snapshots : list[RepositorySnapshot], filepath : str):

    if len(snapshots) == 0:
        return
    
    path = Path(f"{filepath}.json")

    path.parent.mkdir(
        parents = True,
        exist_ok = True
    )

    if path.exists():
        previous_content = path.read_text(encoding = "utf-8")
        if previous_content.strip():
            stored_snapshots = json.loads(previous_content)
        else:
            stored_snapshots = []
    else: 
        stored_snapshots = []

    new_snapshot = [
        asdict(snapshot) for snapshot in snapshots
    ]

    old_keys = {
    (
        snapshot["repository_id"],
        snapshot["captured_at"],
    )
    for snapshot in stored_snapshots
    }

    for snapshot in new_snapshot:
        new_key = (
            snapshot["repository_id"],
            snapshot["captured_at"]
        )
        if new_key not in old_keys: 
            stored_snapshots.append(snapshot)
            old_keys.add(new_key)


    content = json.dumps(
        stored_snapshots,
        indent=4,
        ensure_ascii=False,
    )

    path.write_text(
        content,
        encoding="utf-8",
    )