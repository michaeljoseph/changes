import logging

import sh

from changes import config, shell

log = logging.getLogger(__name__)


def commit_version_change():
    module_name, dry_run, new_version = config.common_arguments()

    commit_result = shell.handle_dry_run(
        sh.git.commit,
        ('-m', new_version, '%s/__init__.py' % module_name, config.CHANGELOG)
    )

    if commit_result:
        push_result = shell.handle_dry_run(sh.git.push, ())
        if not push_result:
            raise Exception('Version change commit failed')


def tag():
    _, dry_run, new_version = config.common_arguments()

    tag_result = shell.handle_dry_run(
        sh.git.tag,
        ('-a', new_version, '-m', '"%s"' % new_version)
    )

    if tag_result:
        push_tags_result = shell.handle_dry_run(sh.git.push, ('--tags'))
        if not push_tags_result:
            raise Exception('Tagging failed')
