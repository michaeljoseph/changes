from unittest2 import TestCase

from changes import config, shell


class ShellTestCase(TestCase):

    def test_handle_dry_run(self):
        config.arguments['--dry-run'] = False
        self.assertEquals(
            '',
            shell.dry_run('diff README.md README.md')
        )

    def test_handle_dry_run_true(self):
        config.arguments['--dry-run'] = True
        self.assertTrue(
            shell.dry_run('diff README.md README.md')
        )
