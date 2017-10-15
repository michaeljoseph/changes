from changes import shell


def test_handle_dry_run(git_repo):
    assert '' == shell.dry_run('diff README.md README.md', False)


def test_handle_dry_run_true(git_repo):
    assert shell.dry_run('diff README.md README.md', True)
