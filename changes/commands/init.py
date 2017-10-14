import os
import click
from ..models import GitRepository



AUTH_TOKEN_ENVVAR = 'GITHUB_AUTH_TOKEN'
STYLES = {
    'info': {
        'fg': 'green',
        'bold': True,
    },
    'note': {
        'fg': 'blue',
        'bold': True,
    },
    'error': {
        'fg': 'red',
        'bold': True,
    }
}


def _echo(message, style):
    click.secho(
        '{}...'.format(message),
        **STYLES[style]
    )


def info(message):
    _echo(message, 'info')


def note(message):
    _echo(message, 'note')


def error(message):
    _echo(message, 'error')


def init():
    """
    Detects, prompts and initialises the project.
    """
    info('Indexing repository')
    repository = GitRepository()

    info('Looking for github auth token in the environment')
    auth_token = os.environ.get(AUTH_TOKEN_ENVVAR)

    if not auth_token:
        info('No auth token found, asking for it')
        note('You need a GitHub token for changes to create a release.')
        click.pause('Press [enter] to launch the GitHub "New personal access '
                    'token" page, to create a token for changes.')
        click.launch('https://github.com/settings/tokens/new')
        auth_token = click.prompt('Enter your changes token')

        dot_env = open('.env').readlines() if os.path.exists('.env') else []
        if AUTH_TOKEN_ENVVAR not in dot_env:
            dot_env.append('{}={}'.format(
                AUTH_TOKEN_ENVVAR,
                auth_token)
            )
            note('Appending {} setting to .env file'.format(AUTH_TOKEN_ENVVAR))
            open('.env', 'w').writelines(dot_env)

    repository.auth_token = auth_token

    info('Fetching pull requests')
    for pull_request in repository.pull_requests:
        note('#{} {} by @{}'.format(
            pull_request.number,
            pull_request.title,
            pull_request.author
        ))
    error('Just kidding')

    return repository
