import click

from . import __version__
from . import commands


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
@click.pass_context
def main(context, dry_run, verbose):
    """Ch-ch-changes"""
    pass


# main.add_command(help_command, name='help')
@click.command()
def init():
    """
    Detects, prompts and initialises the project.
    """
    commands.init()

main.add_command(init)
# main.add_command(status)
# main.add_command(stage)
# main.add_command(publish)


