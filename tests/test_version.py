import mock
from unittest2 import TestCase
from click.testing import CliRunner

from changes import cli, version
from . import BaseTestCase


class BumpVersionTest(TestCase):

    def test_bump_version(self):
        runner = CliRunner()
        result = runner.invoke(cli.main, '--dry-run -p --no-input changes bump_version'.split(' '))
        assert result.exit_code == 0


class VersionTestCase(TestCase):

    def test_increment(self):
        self.assertEquals(
            '1.0.0',
            version.increment('0.0.1', major=True)
        )

        self.assertEquals(
            '0.1.0',
            version.increment('0.0.1', minor=True)
        )

        self.assertEquals(
            '1.0.1',
            version.increment('1.0.0', patch=True)
        )


class VersionApplicationTestCase(BaseTestCase):

    def test_current_version(self):
        self.assertEquals(
            '0.0.1',
            version.current_version(self.module_name)
        )

    def test_get_new_version(self):
        with mock.patch('__builtin__.raw_input') as mock_raw_input:
            mock_raw_input.return_value = None
            self.assertEquals(
                '0.1.0',
                version.get_new_version(
                    self.module_name,
                    '0.0.1',
                    True,
                    minor=True,
                )
            )
