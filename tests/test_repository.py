from changes import models


def test_repository_parses_remote_url(git_repo):
    repository = models.GitRepository()
    assert 'test_app' == repository.repo
    assert 'michaeljoseph' == repository.owner


def test_merged_pull_requests(git_repo_with_merge_commit):
    repository = models.GitRepository()
    assert 1 == len(repository.pull_requests)
    assert '111' == repository.pull_requests[0].number
