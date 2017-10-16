import os
import textwrap

from plumbum.cmd import git

from changes.commands import init
from .conftest import AUTH_TOKEN_ENVVAR


def test_init_prompts_for_auth_token_and_writes_dot_env(
    capsys,
    git_repo_with_merge_commit,
    with_auth_token_prompt
):
    git('tag', '0.0.2')
    git('tag', '0.0.3')

    init.init()

    expected_output = textwrap.dedent(
        """\
        Indexing repository...
        Looking for Github Auth Token in the environment...
        No auth token found, asking for it...
        You need a Github Auth Token for changes to create a release.
        Appending GITHUB_AUTH_TOKEN setting to .env file
        """
    )
    out, _ = capsys.readouterr()
    assert expected_output == out

    assert os.path.exists('.env')
    assert '{}=foo'.format(AUTH_TOKEN_ENVVAR) == open('.env').read()


def test_init_finds_auth_token_in_environment(
    capsys,
    git_repo_with_merge_commit,
    with_auth_token_envvar
):
    git('tag', '0.0.2')
    git('tag', '0.0.3')

    init.init()

    expected_output = textwrap.dedent(
        """\
        Indexing repository...
        Looking for Github Auth Token in the environment...
        Found Github Auth Token in the environment...
        """
    )
    out, _ = capsys.readouterr()
    assert expected_output == out
