import os
import click
from ..models import GitRepository



def _echo(message, **kwargs):
    click.echo(click.style(
        message,
        **kwargs
    ))


def info(message):
    _echo(
        message,
        fg='green',
        bold=True
    )


def note(message):
    _echo(
        message,
        fg='blue',
        bold=True
    )


def init():
    """
    Detects, prompts and initialises the project.
    """
    info('Indexing repository...')
    repository = GitRepository()

    info('Looking for github auth token in the environment...')
    auth_token = os.environ.get('GITHUB_AUTH_TOKEN')

    if not auth_token:
        info('No auth token found, asking for it...')
        note('You need a GitHub token for changes to create a release.')
        click.pause('Press [enter] to launch the GitHub "New personal access '
                    'token" page, to create a token for changes.')
        click.launch('https://github.com/settings/tokens/new')
        auth_token = click.prompt('Enter your changes token')
        repository.auth_token = auth_token

    info('Fetching pull requests...')

    return repository
