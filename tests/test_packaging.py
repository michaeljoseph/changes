from click.testing import CliRunner

from changes import cli

from . import BaseTestCase


class PackagingTestCase(BaseTestCase):
    runner = CliRunner()

    def test_install(self):
        result = self.runner.invoke(cli.main, '-p --no-input --dry-run test_app install'.split(' '))
        assert result.exit_code == 0


    def test_upload(self):
        result = self.runner.invoke(cli.main, '-p --no-input --dry-run test_app upload'.split(' '))
        assert result.exit_code == 0

    def test_pypi(self):
        result = self.runner.invoke(cli.main, '-p --no-input --dry-run test_app pypi'.split(' '))
        assert result.exit_code == 0

