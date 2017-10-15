import click
import requests_cache

from . import __version__
from changes.commands import init as init_command

VERSION = 'changes {}'.format(__version__)


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
    requests_cache.install_cache(
        cache_name='github_cache',
        backend='sqlite',
        expire_after=180000
    )


@click.command()
def init():
    """
    Detects, prompts and initialises the project.
    """
    init_command.init()

main.add_command(init)
