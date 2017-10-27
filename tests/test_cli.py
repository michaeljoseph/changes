from click.testing import CliRunner

import changes
from changes.cli import main


def test_version():
    runner = CliRunner()
    result = runner.invoke(main, ['--version'])
    assert result.exit_code == 0
    assert result.output == 'changes {}\n'.format(changes.__version__)
