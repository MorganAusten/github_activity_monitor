from app.models.repository import Repository
from app.repository_filter import repository_filter

def test_repository_filter():
    repositories = [
        Repository(id = 1, owner="user1", name="repo1", html_url="http://example.com/repo1",
         language="Python", stars=150, created_at="2023-01-01T00:00:00Z", updated_at="2023-01-02T00:00:00Z"),
        Repository(id = 1, owner="user1", name="repo2", html_url="http://example.com/repo2",
         language="Javascript", stars=500, created_at="2023-01-01T00:00:00Z", updated_at="2023-01-02T00:00:00Z"),
        Repository(id = 1, owner="user1", name="repo3", html_url="http://example.com/repo3",
         language="Python", stars=300, created_at="2023-01-01T00:00:00Z", updated_at="2023-01-02T00:00:00Z")
    ]
    filtered_repositories = repository_filter(repositories, language="Python", stars=150)
    print("Hello")

    assert len(filtered_repositories) == 2
    assert filtered_repositories[0].name == "repo1"
    assert filtered_repositories[1].name == "repo3"