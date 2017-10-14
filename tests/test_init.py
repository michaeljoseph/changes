from changes.commands import init


def test_init_prompts_for_auth_token_and_returns_repo(mocker, git_repo):
    launch = mocker.patch('changes.commands.init.click.launch')

    prompt = mocker.patch('changes.commands.init.click.prompt')
    prompt.return_value = 'foo'

    repository = init.init()
    assert 'test_app' == repository.repo
    assert 'foo' == repository.auth_token
