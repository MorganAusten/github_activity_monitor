from pathlib import Path


def write_text_file(content: str, file_path: str) -> None:
    path = Path(file_path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        mode="w",
        encoding="utf-8",
    ) as file:
        file.write(content)