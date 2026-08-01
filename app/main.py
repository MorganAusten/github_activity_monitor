import requests

from pprint import pprint
from app.github_client import GitHubClient
from app.mappers.repository_mapper import repository_from_github

def main() -> None:
    username = input("Username:").strip()

    client = GitHubClient()

    try:
        raw_repositories = client.get_public_repositories(username)
        repositories = [repository_from_github(repository) for repository in raw_repositories]
        
    except ValueError as error:
        print(f"Input Invalid: {error}")
        return
    except requests.Timeout:
        print("GitHub Answered too slowly")
        return
    except requests.ConnectionError:
        print("Impossible to connect to GitHub")
        return
    except requests.HTTPError as error:
        print(f" HTTP GitHub error : {error}")
        return
    except requests.JSONDecodeError:
        print("GitHub returned invalid HTTP response.")
        return


    # pprint(raw_repositories[0])
    # return

    print(f"\n{len(repositories)} depos found. \n")

    for repository in repositories:
        print(f"{repository.owner} | {repository.name} | {repository.language} | {repository.stars} stars")



if __name__ == "__main__":
    main()