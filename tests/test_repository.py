from changes import models
from plumbum.cmd import git


def test_repository_parses_remote_url(git_repo):
    repository = models.GitRepository()
    assert 'test_app' == repository.repo
    assert 'michaeljoseph' == repository.owner


def test_merged_pull_requests(git_repo):
    github = 'Merge pull request #111 from michaeljoseph/appveyor'
    git('commit', '--allow-empty', '-m', github)

    pull_requests = models.merged_pull_requests()
    assert 1 == len(pull_requests)

    assert pull_requests[0].pr_number == '111'
