from click.testing import CliRunner

import changes
from changes.cli import main


def test_version():
    runner = CliRunner()
    result = runner.invoke(main, ['--version'])
    assert result.exit_code == 0
    assert result.output == f'changes {changes.__version__}\n'
