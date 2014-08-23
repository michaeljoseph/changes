from click.testing import CliRunner

from changes import cli, vcs
from . import BaseTestCase


class VcsTestCase(BaseTestCase):
    runner = CliRunner()

    def test_commit_version_change(self):
        vcs.commit_version_change(self.context)

    def test_tag(self):
        result = self.runner.invoke(cli.main, '-p --no-input --dry-run test_app tag'.split(' '))
        assert result.exit_code == 0
