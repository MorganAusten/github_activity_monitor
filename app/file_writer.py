from pathlib import Path
from datetime import datetime


def write_text_file(content: str, file_path: str, extension: str = "md") -> Path:

    extension = extension.lstrip(".")
    timestamp = datetime.now().strftime("%d-%m-%Y_%Hh-%Mm-%Ss")

    file_path = f"{file_path}_{timestamp}.{extension}"

    path = Path(file_path)
    print(file_path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    
    with path.open(
        mode="w",
        encoding="utf-8",
    ) as file:
            file.write(content)

    return path