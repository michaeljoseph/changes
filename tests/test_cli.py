import textwrap

from click.testing import CliRunner

import changes
from changes.cli import main


def test_version():
    runner = CliRunner()
    result = runner.invoke(main, ['--version'])
    assert result.exit_code == 0
    assert result.output == 'changes %s\n' % changes.__version__


def test_init(git_repo_with_merge_commit):
    result = CliRunner().invoke(
        main,
        ['init'],
        env={'GITHUB_AUTH_TOKEN': 'foo'},
    )
    assert result.exit_code == 0

    expected_output = textwrap.dedent(
        """\
        Indexing repository...
        Looking for Github auth token in the environment...
        """
    )
    assert expected_output == result.output


