from changes.commands import init


def test_init_returns_git_repo(git_repo):
    assert 'test_app' == init().repo

