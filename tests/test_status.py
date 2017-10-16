import os

from plumbum.cmd import git
from semantic_version import Version

from changes.commands import status


def test_status(capsys, mocker, git_repo_with_merge_commit):
    _ = mocker.patch('changes.commands.init.click.launch')

    prompt = mocker.patch('changes.commands.init.click.prompt')
    prompt.return_value = 'foo'

    if os.environ.get(init.AUTH_TOKEN_ENVVAR):
        del os.environ[init.AUTH_TOKEN_ENVVAR]

    git('tag', '0.0.2')
    git('tag', '0.0.3')

    status.status()

    expected_output = textwrap.dedent(
        """Indexing repository...
        Looking for Github auth token in the environment...
        Repository: michaeljoseph/test_app...
        Latest Version...
        0.0.1
        Changes...
        """
    )
    out, err = capsys.readouterr()
    assert expected_output == out
    assert '' == err