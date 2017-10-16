import os

from semantic_version import Version

from changes import models


def test_repository_parses_remote_url(git_repo):
    repository = models.GitRepository()
    assert 'test_app' == repository.repo
    assert 'michaeljoseph' == repository.owner


def test_repository_parses_versions(git_repo_with_merge_commit):
    repository = models.GitRepository()

    v1 = Version('0.0.1')
    assert [v1] == repository.versions

    assert v1 == repository.latest_version


def test_unreleased_version(git_repo):
    repository = models.GitRepository()

    assert 0 == len(repository.versions)

    assert Version('0.0.0') == repository.latest_version
