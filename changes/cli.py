import contextlib
import os

import click
import requests_cache

from . import __version__
from changes.commands import init as init_command
from changes.commands import status as status_command
from changes.commands import stage as stage_command

VERSION = 'changes {}'.format(__version__)


@contextlib.contextmanager
def work_in(dirname=None):
    """
    Context manager version of os.chdir. When exited, returns to the working
    directory prior to entering.
    """
    curdir = os.getcwd()
    try:
        if dirname is not None:
            os.chdir(dirname)
        yield
    finally:
        os.chdir(curdir)


def print_version(context, param, value):
    if not value or context.resilient_parsing:
        return
    click.echo(VERSION)
    context.exit()


@click.option(
    '--dry-run',
    help='Prints (instead of executing) the operations to be performed.',
    is_flag=True,
    default=False,
)
@click.option(
    '--verbose',
    help='Enables verbose output.',
    is_flag=True,
    default=False,
)
@click.version_option(
    __version__,
    '-V',
    '--version',
    message=VERSION
)
@click.group(
    context_settings=dict(
        help_option_names=[u'-h', u'--help']
    ),
)
def main(dry_run, verbose):
    """Ch-ch-changes"""


@click.command()
def init():
    """
    Detects, prompts and initialises the project.
    """
    init_command.init()

main.add_command(init)


@click.command()
@click.argument('repo_directory', required=False)
def status(repo_directory):
    """
    Shows current project release status.
    """
    repo_directory = repo_directory if repo_directory else '.'

    with work_in(repo_directory):
        requests_cache.configure()
        status_command.status()

main.add_command(status)


@click.command()
@click.option(
    '--draft',
    help='Enables verbose output.',
    is_flag=True,
    default=False,
)
def stage(draft):
    """
    Stages a release
    """
    requests_cache.configure(expire_after=60*10*10)
    stage_command.stage(draft)

main.add_command(stage)
