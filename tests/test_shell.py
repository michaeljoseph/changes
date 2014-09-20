from unittest2 import TestCase

from changes import config, shell


class ShellTestCase(TestCase):

    def test_handle_dry_run(self):
        self.assertEquals(
            '',
            shell.dry_run('diff README.md README.md', False)
        )

    def test_handle_dry_run_true(self):
        self.assertTrue(
            shell.dry_run('diff README.md README.md', True)
        )
