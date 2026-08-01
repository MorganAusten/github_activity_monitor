from typing import Any

import requests

GITHUB_API_URL = "https://api.github.com"

class GitHubClient:
    def __init__(self,timeout : float = 10.0) -> None:
        self.timeout = timeout

    def get_public_repositories(self, username : str) -> list[dict[str,Any]]:
        username = username.strip()

        if not username:
            raise ValueError("The GitHub username is required")
    
        url = f"{GITHUB_API_URL}/users/{username}/repos"
    
        response = requests.get(
            url,
            headers = {
                "Accept" : "application/vnd.github+json",
                "User-Agent" : "github-activity-monitor",
            },
            params ={
                "per page" : 100,
                "sort" : "updated",
            },
            timeout = self.timeout,
        )
        
        if response.status_code ==404:
            raise ValueError(f"the GitHub user '{username}' doesn't exist.")
    
        response.raise_for_status()
    
        payload = response.json()
    
        if not isinstance(payload, list):
            raise TypeError("The output from GitHub isn't a list.")
    
        return payload