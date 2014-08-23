import logging

import click
from changes import config, shell

log = logging.getLogger(__name__)
pass_changes = click.make_pass_decorator(config.Changes)


def commit_version_change(context):
    shell.dry_run('git commit -m "%s" %s/__init__.py %s' % (context.new_version, context.module_name, config.CHANGELOG), context.dry_run)
    shell.dry_run('git push', context.dry_run)


@click.command()
@pass_changes
def tag(context):
    """Tags your git repo with the new version number"""
    shell.dry_run('git tag -a %s -m "%s"' % (context.new_version, context.new_version), context.dry_run)
    shell.dry_run('git push --tags', context.dry_run)
