from changes import config, shell

from . import *


def test_handle_dry_run():
    assert '' == shell.dry_run('diff README.md README.md', False)


def test_handle_dry_run_true():
    assert shell.dry_run('diff README.md README.md', True)
