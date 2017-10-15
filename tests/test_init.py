import os

import responses

from changes.commands import init


@responses.activate
def test_init_prompts_for_auth_token_and_returns_repo(mocker, git_repo_with_merge_commit):
    _ = mocker.patch('changes.commands.init.click.launch')

    prompt = mocker.patch('changes.commands.init.click.prompt')
    prompt.return_value = 'foo'

    responses.add(
        responses.GET,
        'https://api.github.com/repos/michaeljoseph/test_app/pulls/111',
        json={
            'title': 'The title of the pull request',
            'body': 'An optional, longer description.',
            'user': {
                'login': 'someone'
            }
        },
        status=200,
        content_type='application/json'
    )

    if os.environ.get(init.AUTH_TOKEN_ENVVAR):
        del os.environ[init.AUTH_TOKEN_ENVVAR]

    from plumbum.cmd import git
    git('tag', '0.0.3')
    git('tag', '0.0.1')
    git('tag', '0.0.2')
    repository = init.init()

    assert 'test_app' == repository.repo
    assert 'michaeljoseph' == repository.owner
    assert repository.github

    assert 'foo' == repository.auth_token
    assert os.path.exists('.env')
    assert '{}=foo'.format(init.AUTH_TOKEN_ENVVAR) == open('.env').read()

    assert 1 == len(repository.pull_requests)
    first_pull_request = repository.pull_requests[0]
    assert 'someone' == first_pull_request.author
    assert 'The title of the pull request' == first_pull_request.title

    from semantic_version import Version
    assert [Version('0.0.1'), Version('0.0.2'), Version('0.0.3')] == repository.versions

