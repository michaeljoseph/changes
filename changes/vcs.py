import logging

import sh

from changes import config, shell

log = logging.getLogger(__name__)


def commit_version_change():
    module_name, dry_run, new_version = config.common_arguments()

    shell.handle_dry_run(
        sh.git.commit,
        ('-m', new_version, '%s/__init__.py' % module_name, config.CHANGELOG)
    )

    shell.handle_dry_run(sh.git.push, ())


def tag():
    _, dry_run, new_version = config.common_arguments()

    shell.handle_dry_run(
        sh.git.tag,
        ('-a', new_version, '-m', '"%s"' % new_version)
    )

    shell.handle_dry_run(sh.git.push, ('--tags'))
