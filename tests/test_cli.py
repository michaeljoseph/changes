import textwrap

from click.testing import CliRunner

import changes
from changes.cli import main
from .conftest import AUTH_TOKEN_ENVVAR


def test_version():
    runner = CliRunner()
    result = runner.invoke(main, ['--version'])
    assert result.exit_code == 0
    assert result.output == 'changes %s\n' % changes.__version__


def test_init(git_repo_with_merge_commit):
    result = CliRunner().invoke(
        main,
        ['init'],
        env={AUTH_TOKEN_ENVVAR: 'foo'},
    )
    assert result.exit_code == 0

    expected_output = textwrap.dedent(
        """\
        Indexing repository...
        Looking for Github Auth Token in the environment...
        Found Github Auth Token in the environment...
        """
    )
    assert expected_output == result.output


def test_status(git_repo):
    result = CliRunner().invoke(
       main,
       ['status'],
       env={AUTH_TOKEN_ENVVAR: 'foo'},
    )
    assert 0 == result.exit_code

    expected_output = textwrap.dedent(
        """\
        Indexing repository...
        Looking for Github Auth Token in the environment...
        Found Github Auth Token in the environment...
        Repository: michaeljoseph/test_app...
        Latest Version...
        0.0.0
        Changes...
        0 changes found since 0.0.0
        """
    )
    assert expected_output == result.output
