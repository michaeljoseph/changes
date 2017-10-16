import textwrap
import os

from plumbum.cmd import git
from semantic_version import Version

from changes.commands import status


def test_status(
    capsys,
    git_repo_with_merge_commit,
    with_auth_token_envvar
):

    git('tag', '0.0.2')

    status.status()

    expected_output = textwrap.dedent(
        """\
        Indexing repository...
        Looking for Github auth token in the environment...
        Repository: michaeljoseph/test_app...
        Latest Version...
        0.0.2
        Changes...
        0 changes found since 0.0.2
        """
    )
    out, err = capsys.readouterr()
    assert expected_output == out
    assert '' == err
