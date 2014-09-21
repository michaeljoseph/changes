import logging

import click
from changes import shell

log = logging.getLogger(__name__)


def commit_version_change(context):
    shell.dry_run('git commit -m "%s" %s/__init__.py CHANGELOG.md' % (context.new_version, context.module_name), context.dry_run)
    shell.dry_run('git push', context.dry_run)


def tag_and_push(context):
    """Tags your git repo with the new version number"""
    shell.dry_run('git tag -a %s -m "%s"' % (context.new_version, context.new_version), context.dry_run)
    shell.dry_run('git push --tags', context.dry_run)
