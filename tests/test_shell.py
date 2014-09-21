from unittest2 import TestCase

from changes import shell

from . import context, setup, teardown


def test_handle_dry_run():
    assert '' == shell.dry_run('diff README.md README.md', False)


def test_handle_dry_run_true():
    assert shell.dry_run('diff README.md README.md', True)
