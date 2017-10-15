import responses
from semantic_version import Version

from changes import models


def test_repository_parses_remote_url(git_repo):
    repository = models.GitRepository()
    assert 'test_app' == repository.repo
    assert 'michaeljoseph' == repository.owner


@responses.activate
def test_merged_pull_requests(git_repo_with_merge_commit):
    responses.add(
        responses.GET,
        'https://api.github.com/repos/michaeljoseph/test_app/pulls/111',
        json={
            'title': 'The title of the pull request',
            'body': 'An optional, longer description.',
            'user': {
                'login': 'someone'
            },
        },
        status=200,
        content_type='application/json'
    )

    repository = models.GitRepository()
    assert 1 == len(repository.pull_requests)

    first_pull_request = repository.pull_requests[0]
    assert '111' == first_pull_request.number
    assert [] == repository.versions

    assert Version('0.0.0') == repository.latest_version
