import requests
import app.reports.repository_reporter as repos_reporter 

from datetime import datetime
from app.models.repository_snapshot import make_repository_snapshot
from app.database.json_snapshot_repository import save_snapshots_as_json
from app.github_client import GitHubClient
from app.mappers.repository_mapper import map_repository_from_github
from app.repository_filter import repository_filter
from app.reports.markdown_report import generate_markdown_report
from app.file_writer import write_text_file

def main() -> None:
    username = input("Username:").strip()

    client = GitHubClient()

    try:
        raw_repositories = client.get_public_repositories(username)
        repositories = [map_repository_from_github(repository) for repository in raw_repositories]
        
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

    print(f"\n{len(repositories)} depos found. \n")
    print("All repositories:")
    for repository in repositories:
        print(f"{repository.owner} | {repository.name} | {repository.language} | {repository.stars} stars")



    # pprint(raw_repositories[0])
    # return


    filtered_repositories_a = repository_filter(repositories, language="HTML", stars=100)
    print(f"\n{len(filtered_repositories_a)} repos found. \n")
    print("Filtered repositories_a (params: language = HTML , stars = 100):")
    for repository in filtered_repositories_a:
        print(f"{repository.owner}/{repository.name} | {repository.language} | {repository.stars} stars")

    # filtered_repositories_b = repository_filter(repositories, language= None, stars=1000)
    # filtered_repositories_c = repository_filter(repositories, language= "Ruby", stars=500)
    # print(f"\n{len(filtered_repositories_b)} repos found. \n")
    # print("Filtered repositories_b (params: language = None, stars = 1000):")
    # for repository in filtered_repositories_b:
    #     print(f"{repository.owner}/{repository.name} | {repository.language} | {repository.stars} stars")

    # print(f"\n{len(filtered_repositories_c)} repos found. \n")
    # print("Filtered repositories_c (params: language = Ruby, stars = 500):")
    # for repository in filtered_repositories_c:
    #     print(f"{repository.owner}/{repository.name} | {repository.language} | {repository.stars} stars")

    # test_repository_filter()

    markdown = generate_markdown_report(repos_reporter.build_repository_report(repositories))
    print(generate_markdown_report(repos_reporter.build_repository_report(repositories)))

    created_file =  write_text_file(markdown, "reports/github_report")
    print(f"Created file: {created_file}")

    captured_at = datetime.now()

    snapshots = [
    make_repository_snapshot(repository, captured_at)
    for repository in repositories
]
    save_snapshots_as_json(snapshots, "data/repostory_snapshots" )
    save_snapshots_as_json(snapshots, "data/repostory_snapshots" )

if __name__ == "__main__":
    main()