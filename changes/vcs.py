import logging

from changes import config, shell

log = logging.getLogger(__name__)


def commit_version_change():
    module_name, _, new_version = config.common_arguments()
    shell.dry_run('git commit -m "%s" %s/__init__.py %s' % (new_version, module_name, config.CHANGELOG))
    shell.dry_run('git push')


def tag():
    _, dry_run, new_version = config.common_arguments()
    shell.dry_run('git tag -a %s -m "%s"' % (new_version, new_version))
    shell.dry_run('git push --tags')
