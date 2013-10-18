from changes import config, shell


def commit_version_change():
    app_name, dry_run, new_version = config.common_arguments()

    command = 'git commit -m %s %s/__init__.py %s' % (
        new_version, app_name, config.CHANGELOG
    )

    if not (shell.execute(command, dry_run=dry_run) and
            shell.execute('git push', dry_run=dry_run)):
        raise Exception('Version change commit failed')

def tag():
    _, dry_run, new_version = config.common_arguments()

    shell.execute(
        'git tag -a %s -m "%s"' % (new_version, new_version),
        dry_run=dry_run
    )
    shell.execute('git push --tags', dry_run=dry_run)
