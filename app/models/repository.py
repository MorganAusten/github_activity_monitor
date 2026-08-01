from dataclasses import dataclass

@dataclass

class Repository:
    id : int
    owner : str
    name : str
    html_url : str
    language : str | None
    stars : int
    created_at : str
    updated_at: str

